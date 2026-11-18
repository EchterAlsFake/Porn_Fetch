# GUI translations

The 4.0 target languages are German (Germany), neutral Spanish, Hindi (India)
and Simplified Chinese (mainland China). The CLI uses English. The GUI
language is separate from the setting that requests localized provider titles.

## Generate translations

In GitHub Actions, run **Generate GUI translations** on a trusted branch.
Configure the repository secret `OPENAI_API_KEY` first. The workflow generates
all missing messages by default. Select one locale and a small limit for a pilot.
The run uploads TS catalogs and, on success, a patch with the regenerated
resources. Review the changes in a pull request before merging. The workflow
has read-only repository permissions.

From a development checkout with the GUI extras installed:

```sh
uv run --no-sync python scripts/translations.py extract
uv run --no-sync python scripts/translations.py context --locale hi_IN --limit 5 > context.json
uv run --no-sync python scripts/translations.py generate
uv run --no-sync python scripts/translations.py extract
uv run --no-sync python scripts/translations.py check
uv run --no-sync python scripts/translations.py build
```

`context` exports the prompt and pending messages offline. `generate` sends the
same source context to the OpenAI Responses API, using `OPENAI_API_KEY` from the
environment. The default model is `gpt-6.1-terra`. Use `--model` or
`OPENAI_TRANSLATION_MODEL` to select another model with Structured Outputs.
The generator sends repository copy and bounded source excerpts. It has no
access to app users' accounts, downloads, settings, or runtime data.
Every accepted batch is saved to the TS catalog. Rerunning resumes at the
remaining unfinished messages and preserves finished translations. Set a
message back to unfinished to regenerate it. [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)

## Maintain context

Keep product terminology and workflows in
[TRANSLATION_CONTEXT.md](TRANSLATION_CONTEXT.md). The generator sends that guide
with the exact source message, Qt context, disambiguation, nearby code, and
translator notes. For example, the note on the compact **+ Add** button
explains that it opens the creator subscription form. The surrounding code
also shows the relevant availability checks.

- In QML put a `//:` translator note immediately above a translation call.
  Add the second argument of `qsTr()` when identical English needs separate
  translations for different meanings.
- In Python use `#:` above `self.tr()`, and explain ambiguous actions or
  placeholder values. Qt-free shared modules can use `QT_TRANSLATE_NOOP` on
  English copy that the GUI resolves with `QCoreApplication.translate`.
- Keep sentences together. Use reorderable placeholders such as `%1` in QML
  and `%(name)s` in Python. Use Qt numerus for a single count, give the English
  catalog its singular and plural forms, and keep stored IDs separate from labels.

## Review in the app

Build resources, then launch from the environment below to include partial
catalogs. In desktop Settings or mobile Settings → Appearance, pick the
language and restart. Mobile layout can also be previewed with `--android`.

```sh
PORN_FETCH_PREVIEW_TRANSLATIONS=1 uv run --no-sync python main.py
```

On PowerShell, set `$env:PORN_FETCH_PREVIEW_TRANSLATIONS = "1"` before launching.
Normal builds offer a target locale once all current entries pass catalog
validation. Missing draft entries fall back to English. System default follows
the OS's preferred languages when a matching catalog is available. Native system UI follows its platform's language support. The bundled legal
agreement and third-party notices are displayed verbatim.

Review the desktop and mobile layouts, especially first-run consent, license
copy, errors, plural forms, potentially clipped controls, and keyboard or
D-pad focus. Catalog validation checks source coverage, protected tokens,
plural form counts, and compilation. It does not evaluate translation quality.
After review, commit TS catalogs and generated QM files, the resource manifest,
and `resources.py`.
