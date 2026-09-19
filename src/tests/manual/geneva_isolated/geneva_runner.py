#!/usr/bin/env python3
"""Run Geneva and one command in the same already-isolated network namespace."""

from __future__ import annotations

import argparse
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--geneva-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--ports", default="80,443")
    parser.add_argument("--strategy", default=r"\/")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if args.command[:1] == ["--"]:
        args.command = args.command[1:]
    if not args.command:
        parser.error("a command is required after --")
    return args


def terminate_process_group(process: subprocess.Popen[bytes], timeout: float = 8.0) -> None:
    if process.poll() is not None:
        return
    try:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=timeout)
    except ProcessLookupError:
        return
    except subprocess.TimeoutExpired:
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait()


def main() -> int:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    ready_path = args.output_dir / "geneva.ready"

    sys.path.insert(0, str(args.geneva_dir))
    import engine as geneva_engine  # pylint: disable=import-outside-toplevel

    class IsolatedEngine(geneva_engine.Engine):
        """Avoid reserializing untouched inbound packets on modern Scapy."""

        def in_callback(self, nfpacket: object) -> None:
            if self.strategy.in_actions:
                super().in_callback(nfpacket)
                return
            if not self.running_nfqueue:
                return
            packet = geneva_engine.layers.packet.Packet(
                geneva_engine.IP(nfpacket.get_payload())
            )
            if self.save_seen_packets:
                self.seen_packets.append(packet)
            self.logger.debug("Received unmodified inbound packet: %s", packet)
            nfpacket.accept()

    stop_requested = threading.Event()
    app_process: subprocess.Popen[bytes] | None = None

    def request_stop(_signum: int, _frame: object) -> None:
        stop_requested.set()

    signal.signal(signal.SIGINT, request_stop)
    signal.signal(signal.SIGTERM, request_stop)

    environment_id = f"pornfetch-{int(time.time())}"
    try:
        with IsolatedEngine(
            args.ports,
            args.strategy,
            environment_id=environment_id,
            output_directory=str(args.output_dir / "geneva"),
            log_level="info",
            file_log_level="debug",
            save_seen_packets=True,
        ):
            ready_path.write_text(
                f"pid={os.getpid()}\nports={args.ports}\nstrategy={args.strategy}\n",
                encoding="utf-8",
            )
            print(
                f"Geneva is ready in the isolated namespace; artifacts: {args.output_dir}",
                flush=True,
            )
            app_process = subprocess.Popen(
                args.command,
                cwd=os.environ.get("PORNFETCH_PROJECT_DIR"),
                start_new_session=True,
            )
            while app_process.poll() is None and not stop_requested.wait(0.2):
                pass
            if stop_requested.is_set():
                terminate_process_group(app_process)
            return int(app_process.returncode or 0)
    finally:
        ready_path.unlink(missing_ok=True)
        if app_process is not None:
            terminate_process_group(app_process)


if __name__ == "__main__":
    raise SystemExit(main())
