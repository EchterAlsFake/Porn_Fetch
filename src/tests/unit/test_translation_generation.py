"""Verify that the maintainer tool saves only validated translations."""
import io
import json
import tempfile
import unittest
import xml.etree.ElementTree as ET
from argparse import Namespace
from unittest.mock import patch

from scripts import translation_ai
from scripts.translations import ROOT


class TranslationGenerationTests(unittest.TestCase):
    def test_generation_retries_changed_placeholders_and_preserves_finished_entries(self):
        source = "%n record(s) checked"
        pending = f'<message numerus="yes"><source>{source}</source>{{}}</message>'
        finished = '<message><source>Stop</source><translation>Detener</translation></message>'
        location = ET.Element("location", filename="src/frontend/UI/CreatorsPage.qml", line="50")
        note = ET.Element("extracomment")
        note.text = "Progress of the creator library check."
        original = ET.ElementTree(ET.fromstring(
            '<TS><context><name>CreatorsPage</name>' + pending.format("") + finished + '</context></TS>'
        ))
        message = original.find(".//message")
        message.insert(0, location)
        message.append(note)

        with tempfile.TemporaryDirectory() as directory:
            from pathlib import Path

            catalogs = Path(directory)
            catalog = catalogs / "es.ts"
            catalog.write_text(
                '<TS language="es"><context><name>CreatorsPage</name>'
                + pending.format('<translation type="unfinished" />') + finished + '</context></TS>',
                encoding="utf-8",
            )
            calls = []

            def respond(request, timeout):
                body = json.loads(request.data)
                payload = json.loads(body["input"])
                calls.append(payload)
                entry, = payload["messages"]
                self.assertEqual(entry["translator_note"], note.text)
                self.assertEqual(entry["requested_forms"], ["one", "other"])
                self.assertIn("excerpt", entry["locations"][0])
                self.assertFalse(body["store"])
                self.assertTrue(body["text"]["format"]["strict"])
                forms = ["%n registro comprobado", "Sin marcador"]
                if "previous_validation_error" in payload:
                    self.assertIn("changed placeholders", payload["previous_validation_error"])
                    forms[1] = "%n registros comprobados"
                response = json.dumps({"translations": [{"id": entry["id"], "forms": forms}]})
                return io.BytesIO(json.dumps({
                    "status": "completed",
                    "output": [{"type": "message", "content": [{"type": "output_text", "text": response}]}],
                }).encode())

            args = Namespace(command="generate", locale=["es"], model=None, limit=None)
            with patch.dict("os.environ", {"OPENAI_API_KEY": "test"}), \
                    patch.object(translation_ai, "CATALOGS", catalogs), \
                    patch.object(translation_ai, "fresh_catalog", return_value=(original, ROOT)), \
                    patch.object(translation_ai, "urlopen", side_effect=respond):
                translation_ai.context_or_generate(args)
                translation_ai.context_or_generate(args)

            self.assertEqual(len(calls), 2)
            messages = ET.parse(catalog).findall(".//message")
            self.assertEqual([node.text for node in messages[0].findall("translation/numerusform")],
                             ["%n registro comprobado", "%n registros comprobados"])
            self.assertEqual(messages[1].findtext("translation"), "Detener")
