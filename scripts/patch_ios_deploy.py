"""Preserve explicit Qt module selection in PySide6 6.12's iOS deploy tool."""

from pathlib import Path


def main() -> None:
    import PySide6

    if PySide6.__version__ != "6.12.0":
        raise SystemExit("The iOS deployment patch requires PySide6 6.12.0")
    target = Path(PySide6.__file__).parent / "scripts/deploy_lib/config.py"
    source = target.read_text()
    original = "        self.modules = []\n"
    replacement = "        self._modules = []\n"
    if original not in source and source.count(replacement) == 1:
        print("iOS deployment module-selection patch already applied")
        return
    if source.count(original) != 1:
        raise SystemExit(f"Unexpected deployment configuration source: {target}")
    # The public setter also writes the spec parser. Calling it in Config's
    # constructor clears [qt] modules before IOSConfig can read that setting,
    # causing diagnostic-only QtTest imports to enter the static link instead.
    target.write_text(source.replace(original, replacement, 1))
    print(f"Preserved explicit Qt modules in {target}")


if __name__ == "__main__":
    main()
