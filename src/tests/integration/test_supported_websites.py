"""Offline checks for the shared website matrix and both responsive QML pages."""
from __future__ import annotations

import ast
import tempfile
import unittest
from pathlib import Path

from PySide6.QtCore import QObject, QSettings, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlComponent, QQmlEngine

from src.backend.config import SettingsManager
from src.shared.provider_routing import PROVIDER_MODULES

PROJECT = Path(__file__).resolve().parents[3]
UI = PROJECT / "src/frontend/UI"


class SupportedWebsitesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QGuiApplication.instance() or QGuiApplication([])

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.settings = SettingsManager(QSettings(
            str(Path(self.directory.name) / "settings.ini"), QSettings.Format.IniFormat,
        ))
        self.engine = QQmlEngine()
        self.engine.rootContext().setContextProperty("appSettings", self.settings)
        self.warnings = []
        self.engine.warnings.connect(lambda errors: self.warnings.extend(error.toString() for error in errors))
        self.components = []
        self.roots = []

    def tearDown(self):
        for root in self.roots:
            root.deleteLater()
        self.app.sendPostedEvents(None, 0)
        self.engine = None
        self.directory.cleanup()

    def load(self, filename):
        component = QQmlComponent(self.engine, QUrl.fromLocalFile(str(UI / filename)))
        self.components.append(component)
        root = component.create()
        self.assertIsNotNone(root, "\n".join(error.toString() for error in component.errors()))
        self.roots.append(root)
        return root

    def test_shared_matrix_matches_document_and_registered_providers(self):
        catalog = self.load("WebsiteSupportData.qml")
        sites = catalog.property("sites").toVariant()
        self.assertEqual({site["provider"] for site in sites}, set(PROVIDER_MODULES))
        gui_source = ast.parse((PROJECT / "src/backend/clients.py").read_text(encoding="utf-8"))
        registration = next(node.value for node in gui_source.body if isinstance(node, ast.Assign)
                            and any(isinstance(target, ast.Name) and target.id == "SITE_PATTERNS"
                                    for target in node.targets))
        self.assertEqual({entry.elts[0].value for entry in registration.elts}, set(PROVIDER_MODULES))

        document = (PROJECT / "docs/WEBSITES.md").read_text(encoding="utf-8")
        names = {site["name"] for site in sites}
        rows = {}
        for line in document.splitlines():
            if line.startswith("| "):
                cells = [cell.strip() for cell in line.strip("|").split("|")]
                if cells[0] in names:
                    rows[cells[0]] = cells[1:]
        self.assertEqual(set(rows), names)
        for site in sites:
            for frontend in ("gui", "cli"):
                expected = [cell if cell != "CLI only" else ("Yes" if frontend == "cli" else "—")
                            for cell in rows[site["name"]]]
                self.assertEqual(expected, site[frontend], f"{frontend}: {site['name']}")
            self.assertEqual(site["gui"][4], "—")
            self.assertEqual(site["cli"][4], "—")
        self.assertIn("Keyword search is unavailable for legal reasons.", document)

    def test_pages_load_wide_and_narrow_for_both_frontends(self):
        for filename in ("SupportedWebsitesPage.qml", "AndroidSupportedWebsitesPage.qml"):
            page = self.load(filename)
            page.setProperty("height", 800)
            content = page.findChild(QObject, "websiteSupportContent")
            self.assertIsNotNone(content)
            for width in (400, 1280):
                page.setProperty("width", width)
                for frontend in (0, 1):
                    with self.subTest(page=filename, width=width, frontend=frontend):
                        content.setProperty("frontendIndex", frontend)
                        self.app.processEvents()
                        self.assertEqual(content.property("compact"), width == 400)
                        self.assertEqual(self.warnings, [])


if __name__ == "__main__":
    unittest.main()
