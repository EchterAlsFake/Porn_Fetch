"""Offline checks for the desktop provider inventory and manual-only exception."""
import json
import tempfile
import unittest
from pathlib import Path

from src.shared.provider_routing import PROVIDER_MODULES
from src.tests.smoke.download_gui import SCENARIOS, make_report, parse_args, save_report


class DesktopDownloadInventoryTests(unittest.TestCase):
    def test_default_covers_every_provider_without_automating_spankbang(self):
        args = parse_args([])
        automated = {provider for provider, _, _ in args.fixtures}
        self.assertEqual(automated, set(PROVIDER_MODULES) - {"spankbang"})
        self.assertEqual(len(args.fixtures) * len(args.scenarios), 42)
        self.assertEqual({(c["provider"], c["scenario"], c["status"]) for c in args.manual_checks},
                         {("spankbang", scenario, "MANUAL") for scenario in SCENARIOS})

    def test_focused_selection_keeps_native_transport_and_excludes_unselected_providers(self):
        args = parse_args(["--provider", "youporn", "--provider", "xfreehd", "--scenario", "cleanup"])
        self.assertEqual({provider: transport for provider, transport, _ in args.fixtures},
                         {"youporn": "auto", "xfreehd": "raw"})
        self.assertEqual(args.scenarios, ("cleanup",))
        self.assertEqual(args.manual_checks, [])

    def test_explicit_spankbang_is_recorded_as_manual_without_passing_any_case(self):
        args = parse_args(["--provider", "spankbang"])
        self.assertEqual(args.fixtures, [])
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "report.json"
            save_report(make_report(args), path)
            report = json.loads(path.read_text())
        self.assertEqual(report["manual"], 3)
        self.assertEqual(report["planned_cases"], 0)
        self.assertEqual(report["passed"], 0)
        self.assertEqual(report["results"], [])
        self.assertTrue(all(check["status"] == "MANUAL" for check in report["manual_checks"]))
