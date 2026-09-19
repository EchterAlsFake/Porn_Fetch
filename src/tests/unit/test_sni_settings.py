from __future__ import annotations

import unittest
from unittest.mock import patch

from src.backend.config import SettingsManager


class _MemorySettings:
    def __init__(self, values: dict[str, object] | None = None) -> None:
        self.values = dict(values or {})
        self.sync_count = 0

    def value(self, key: str, defaultValue: object = None) -> object:
        return self.values.get(key, defaultValue)

    def setValue(self, key: str, value: object) -> None:
        self.values[key] = value

    def sync(self) -> None:
        self.sync_count += 1

    def clear(self) -> None:
        self.values.clear()


class SNISettingsTests(unittest.TestCase):
    @staticmethod
    def manager(values: dict[str, object]) -> tuple[SettingsManager, _MemorySettings]:
        storage = _MemorySettings(values)
        with patch("src.backend.config.QSettings", return_value=storage):
            manager = SettingsManager()
        return manager, storage

    def test_migrates_legacy_double_selection_to_strict(self) -> None:
        manager, storage = self.manager(
            {
                "Privacy/sni_obfuscation": True,
                "Privacy/sni_obfuscation_lite": True,
                "Privacy/sni_obfuscation_strict": True,
            }
        )

        self.assertFalse(manager.sni_obfuscation_lite)
        self.assertTrue(manager.sni_obfuscation_strict)
        self.assertEqual(storage.sync_count, 1)

    def test_mode_slot_persists_both_values_atomically(self) -> None:
        manager, storage = self.manager(
            {
                "Privacy/sni_obfuscation": True,
                "Privacy/sni_obfuscation_lite": True,
                "Privacy/sni_obfuscation_strict": False,
            }
        )

        manager.set_sni_obfuscation_mode("strict")

        self.assertFalse(storage.values["Privacy/sni_obfuscation_lite"])
        self.assertTrue(storage.values["Privacy/sni_obfuscation_strict"])
        self.assertFalse(manager.sni_obfuscation_lite)
        self.assertTrue(manager.sni_obfuscation_strict)
        self.assertEqual(storage.sync_count, 1)

    def test_enabled_legacy_configuration_without_mode_defaults_to_lite(self) -> None:
        manager, storage = self.manager({"Privacy/sni_obfuscation": True})

        self.assertTrue(manager.sni_obfuscation_lite)
        self.assertFalse(manager.sni_obfuscation_strict)
        self.assertEqual(storage.sync_count, 1)


if __name__ == "__main__":
    unittest.main()
