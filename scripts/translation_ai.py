"""Maintainer-only AI generation from extracted GUI messages and source context."""
import json
import os
import tempfile
import time
import xml.etree.ElementTree as ET
from functools import cache
from itertools import batched
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from scripts import build_output
from scripts.translations import (
    CATALOGS,
    RELEASE_LOCALES,
    ROOT,
    SOURCES,
    form_names,
    fresh_catalog,
    messages,
    protected_tokens,
    validate_forms,
)

BATCH_SIZE = 20
DEFAULT_MODEL = "gpt-6.1-terra"
LOCALE_BRIEFS = {
    "de_DE": "German for Germany. Use concise standard German and neutral phrasing or informal du.",
    "es": "Neutral Spanish for a general international audience. Use consistent singular tú.",
    "hi_IN": "Hindi as used in India, in Devanagari. Use respectful आप and familiar software vocabulary.",
    "zh_CN": "Simplified Chinese as used in mainland China. Use established software terminology.",
}
RESPONSE_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["translations"],
    "properties": {
        "translations": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "forms"],
                "properties": {
                    "id": {"type": "integer"},
                    "forms": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    },
}


@cache
def source_lines(path):
    return path.read_text(encoding="utf-8").splitlines()


def describe(key, message, catalog_directory, locale, index):
    locations = []
    for location in message.findall("location")[:3]:
        path = (catalog_directory / location.attrib["filename"]).resolve()
        if path not in SOURCES:
            raise ValueError(f"unexpected catalog source file: {path}")
        line = int(location.attrib["line"])
        lines = source_lines(path)
        start = max(0, line - 9)
        end = line + 8
        locations.append({
            "file": path.relative_to(ROOT).as_posix(),
            "line": line,
            "first_excerpt_line": start + 1,
            "excerpt": "\n".join(text[:600] for text in lines[start:end]),
        })
    context, source, disambiguation, _ = key
    return {
        "id": index,
        "context": context,
        "source": source,
        "disambiguation": disambiguation,
        "translator_note": message.findtext("extracomment", ""),
        "protected_text": list(protected_tokens(source).elements()),
        "requested_forms": form_names(locale, key),
        "locations": locations,
    }


def openai_response(api_key, model, instructions, payload):
    body = {
        "model": model,
        "store": False,
        "instructions": instructions,
        "input": json.dumps(payload, ensure_ascii=False),
        "text": {"format": {"type": "json_schema", "name": "gui_catalog",
                            "strict": True, "schema": RESPONSE_SCHEMA}},
    }
    request = Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(body).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
    )
    for attempt in range(3):
        try:
            with urlopen(request, timeout=120) as response:
                result = json.load(response)
            break
        except HTTPError as error:
            with error:
                request_id = error.headers.get("x-request-id", "unavailable")
            if attempt == 2 or error.code not in {408, 429, 500, 502, 503, 504}:
                raise SystemExit(f"OpenAI HTTP {error.code}, request ID {request_id}") from None
        except (URLError, TimeoutError) as error:
            if attempt == 2:
                raise SystemExit(f"OpenAI request failed: {type(error).__name__}") from None
        time.sleep(2 ** (attempt + 1))

    content = [part for item in result.get("output", []) if item.get("type") == "message"
               for part in item.get("content", [])]
    if any(part.get("type") == "refusal" for part in content):
        raise SystemExit(f"OpenAI refused a translation batch ({result.get('id', 'no response ID')}).")
    if result.get("status") != "completed":
        raise ValueError(f"OpenAI returned an incomplete response ({result.get('id', 'no response ID')})")
    return json.loads("".join(part["text"] for part in content if part["type"] == "output_text"))


def validated_response(locale, batch, response):
    rows = response["translations"]
    by_id = {row["id"]: row["forms"] for row in rows}
    expected_ids = {entry["id"] for _, _, entry in batch}
    if set(by_id) != expected_ids or len(rows) != len(expected_ids):
        raise ValueError("translation IDs are missing, duplicated or unexpected")
    for key, _, entry in batch:
        validate_forms(locale, key, by_id[entry["id"]])
    return by_id


def save_catalog(path, tree):
    # Match Qt's indentation and save atomically so an interrupted run can resume.
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                     dir=path.parent, delete=False) as output:
        temporary = path.with_name(os.path.basename(output.name))
        try:
            root = tree.getroot()
            attributes = ET.tostring(ET.Element("TS", root.attrib), encoding="unicode").removesuffix(" />")
            output.write(f'<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE TS>\n{attributes}>\n')
            for context in root:
                ET.indent(context, space="    ")
                output.write(ET.tostring(context, encoding="unicode", short_empty_elements=False).rstrip() + "\n")
            output.write("</TS>\n")
            output.close()
            temporary.chmod(path.stat().st_mode & 0o777)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)


def context_or_generate(args):
    generate = args.command == "generate"
    api_key = os.environ.get("OPENAI_API_KEY")
    if generate and not api_key:
        raise SystemExit("Set OPENAI_API_KEY to generate translations, or use context for an offline export.")
    model = args.model or os.environ.get("OPENAI_TRANSLATION_MODEL") or DEFAULT_MODEL
    instructions = (ROOT / "docs/TRANSLATION_CONTEXT.md").read_text(encoding="utf-8")
    fresh, catalog_directory = fresh_catalog()
    source = dict(messages(fresh))
    exported = []
    for locale in args.locale or RELEASE_LOCALES:
        path = CATALOGS / f"{locale}.ts"
        tree = ET.parse(path)
        target = dict(messages(tree))
        if tree.getroot().get("language") != locale or target.keys() != source.keys():
            raise SystemExit(f"{path.name} does not match the current source catalog. Run extract.")
        pending = [key for key, message in target.items() if message.find("translation") is None
                   or message.find("translation").get("type") == "unfinished"]
        pending = pending[:args.limit]
        batch_entries = [(key, target[key], describe(key, source[key], catalog_directory, locale, index))
                         for index, key in enumerate(pending)]
        brief = {"locale": locale, "language_guidance": LOCALE_BRIEFS[locale]}
        if not generate:
            exported.append({**brief, "messages": [entry for _, _, entry in batch_entries]})
            continue

        for batch in batched(batch_entries, BATCH_SIZE):
            payload = {**brief, "messages": [entry for _, _, entry in batch]}
            first = batch[0][2]["id"] + 1
            error_message = ""
            for _ in range(3):
                if error_message:
                    payload["previous_validation_error"] = error_message
                try:
                    result = openai_response(api_key, model, instructions, payload)
                    by_id = validated_response(locale, batch, result)
                    break
                except (KeyError, TypeError, ValueError) as error:
                    error_message = str(error)
            else:
                raise SystemExit(f"{locale} batch starting at message {first} failed: {error_message}")
            for key, message, entry in batch:
                translation = message.find("translation")
                if translation is None:
                    translation = ET.SubElement(message, "translation")
                translation.clear()
                forms = by_id[entry["id"]]
                if key[3]:
                    for form in forms:
                        ET.SubElement(translation, "numerusform").text = form
                else:
                    translation.text = forms[0]
            save_catalog(path, tree)
            build_output.detail(f"{locale}: saved {first + len(batch) - 1}/{len(batch_entries)} pending messages")
        if not batch_entries:
            build_output.detail(f"{locale}: no pending messages")
    if not generate:
        print(json.dumps({"instructions": instructions, "catalogs": exported}, ensure_ascii=False, indent=2))
