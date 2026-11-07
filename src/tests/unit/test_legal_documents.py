"""Legal notices must remain readable in source, frozen builds and PEP 639 wheels."""
import tempfile
import unittest
from importlib.metadata import PathDistribution
from pathlib import Path
from unittest.mock import patch

from src.shared.legal import legal_document


class LegalDocumentTests(unittest.TestCase):
    def test_wheel_metadata_supplies_documents_missing_from_the_installation_root(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            metadata = root / "porn_fetch-3.9.dist-info"
            (metadata / "licenses").mkdir(parents=True)
            for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
                (metadata / "licenses" / name).write_text(f"Wheel document: {name}", encoding="utf-8")
            with patch("src.shared.legal.__file__", str(root / "src/shared/legal.py")), \
                    patch("src.shared.legal.distribution", return_value=PathDistribution(metadata)):
                for name in ("LICENSE", "THIRD_PARTY_NOTICES.md"):
                    self.assertEqual(legal_document(name), f"Wheel document: {name}")

    def test_frozen_bundle_document_takes_precedence_over_installed_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "LICENSE").write_text("Frozen release license", encoding="utf-8")
            with patch("sys._MEIPASS", directory, create=True), patch("src.shared.legal.distribution") as metadata:
                self.assertEqual(legal_document("LICENSE"), "Frozen release license")
                metadata.assert_not_called()
