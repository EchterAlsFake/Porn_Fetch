"""Result model shared by CLI diagnostics."""

from dataclasses import dataclass


@dataclass(slots=True)
class TestResult:
    category: str
    name: str
    target: str
    passed: bool
    details: str
    duration_s: float
    error: str | None = None
