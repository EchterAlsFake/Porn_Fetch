"""Shared beta notice and the minimum reading time for every frontend."""
from __future__ import annotations

import math
import time

BETA_DISCLAIMER_VERSION = "3.9-beta-1"
BETA_DISCLAIMER_READ_SECONDS = 30
BETA_DISCLAIMER_TEXT = """Hi, you are using the Porn Fetch BETA for the upcoming v3.9 release!

This beta is still incomplete, not fully tested and does not represent a finished nor polished product.
The credits section and supported websites section may be incomplete.

Additionally, the licensing system is still in the sandbox environment. You can obtain a Porn Fetch license
FOR FREE.

You do NOT have to buy anything, spend any money nor give your credit card.
Go to: https://pornfetch.to, select the Crypto Checkout, confirm the local simulation and you'll receive
a valid license in under 10 seconds.

If there are any issues with license activation, E-Mail to: support@echteralsfake.me
I am actively hard-working on the final v3.9 release.

By clicking "OK" you actively consent, that you are participating in an experimental beta release.
- Do not blame me if anything goes wrong
- Do not blame me if your data gets lost
- Do not blame me if the privacy poliy doesn't match the actual app yet
- Do not blame me if the terms of service don't match the actual app yet
"""


class DisclaimerReadDelay:
    """Do not allow acceptance until a full reading interval has elapsed."""

    def __init__(self) -> None:
        self._deadline: float | None = None

    def start(self) -> None:
        self._deadline = time.monotonic() + BETA_DISCLAIMER_READ_SECONDS

    @property
    def remaining_seconds(self) -> int:
        if self._deadline is None:
            return BETA_DISCLAIMER_READ_SECONDS
        return max(0, math.ceil(self._deadline - time.monotonic()))
