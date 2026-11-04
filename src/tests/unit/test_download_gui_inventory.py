"""Offline checks for the desktop provider inventory and manual-only exception."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from src.shared.provider_routing import PROVIDER_MODULES
from src.tests.smoke.download_gui import SCENARIOS, make_report, parse_args, save_report
from src.tests.smoke.download_lifecycle import parse_args as lifecycle_args
from src.tests.smoke.download_queue import parse_args as queue_args


class DesktopDownloadInventoryTests(unittest.TestCase):
    def test_cli_media_inventory_keeps_known_cdn_problem_explicitly_manual(self):
        args = lifecycle_args([])
        self.assertEqual({provider for provider, _, _ in args.fixtures}, set(PROVIDER_MODULES) - {"spankbang"})
        self.assertEqual({(row["provider"], row["scenario"], row["status"]) for row in args.manual_checks},
                         {("spankbang", scenario, "MANUAL") for scenario in ("pause-resume", "cleanup")})
        retry = lifecycle_args(["--provider", "spankbang", "--include-manual-providers"])
        self.assertEqual([provider for provider, _, _ in retry.fixtures], ["spankbang"])
        self.assertEqual(retry.manual_checks, [])

    def test_manual_only_cli_run_reports_zero_passes_without_ffmpeg_or_network(self):
        with tempfile.TemporaryDirectory() as directory:
            report = Path(directory) / "result.json"
            result = subprocess.run(
                [sys.executable, "-m", "src.tests.smoke.download_lifecycle", "--provider", "spankbang",
                 "--report", str(report)], capture_output=True, text=True, timeout=10,
                cwd=Path(__file__).resolve().parents[3],
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(report.read_text())
        self.assertEqual(data["passed"], 0)
        self.assertEqual(data["planned_cases"], 0)
        self.assertEqual(data["manual"], 2)
        self.assertEqual(data["results"], [])

    def test_queue_inventory_separates_free_and_premium_workflows(self):
        self.assertEqual(queue_args(["--access", "free"]).cases, [("parallel-1", 1)])
        self.assertEqual(dict(queue_args(["--access", "premium"]).cases),
                         {"premium-parallel-1": 1, "parallel-2": 2, "stop-remove": 2})

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
