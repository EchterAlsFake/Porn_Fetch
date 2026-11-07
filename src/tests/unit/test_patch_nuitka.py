"""Offline checks for import preservation and cache invalidation in the build patch."""
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from scripts import patch_nuitka

# A small scanner fixture keeps these checks independent of Nuitka installation.
# The real upstream source digest is checked separately against the installed tool.
SCANNER = '''def getPEFileUsedDllNames(filename):
    pefile = importFromInlineCopy("pefile", must_exist=True)
    try:
        with pefile.PE(filename) as pe_info:
            pe_info.parse_data_directories(
                directories=(pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_IMPORT"],),
                import_dllnames_only=True,
            )
            pe_info.parse_data_directories(
                directories=(pefile.DIRECTORY_ENTRY["IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT"],),
            )
            result = OrderedSet()
            for entry_name in ("DIRECTORY_ENTRY_IMPORT", "DIRECTORY_ENTRY_DELAY_IMPORT"):
                for entry in getattr(pe_info, entry_name, ()):
                    result.add(entry.dll.decode("utf8"))
            return result
    except pefile.PEFormatError:
        return None
'''


class NuitkaPatchTests(unittest.TestCase):
    def patched_fixture(self):
        with patch.object(patch_nuitka, "SOURCE_DIGEST", patch_nuitka.ast_digest(SCANNER)):
            return patch_nuitka.patch_source(SCANNER)

    def test_regular_and_delayed_imports_are_cached_without_sharing_mutable_results(self):
        pe = Mock()
        pe.__enter__ = Mock(return_value=pe)
        pe.__exit__ = Mock(return_value=False)

        def parse(*, directories, **kwargs):
            name = "DIRECTORY_ENTRY_IMPORT" if directories == (1,) else "DIRECTORY_ENTRY_DELAY_IMPORT"
            setattr(pe, name, [SimpleNamespace(dll=b"normal.dll" if directories == (1,) else b"delayed.dll")])

        pe.parse_data_directories.side_effect = parse
        reader = Mock(return_value=pe)
        module = SimpleNamespace(PE=reader, PEFormatError=ValueError, DIRECTORY_ENTRY={
            "IMAGE_DIRECTORY_ENTRY_IMPORT": 1, "IMAGE_DIRECTORY_ENTRY_DELAY_IMPORT": 13})
        namespace = {"os": os, "OrderedSet": set, "importFromInlineCopy": lambda *args, **kwargs: module}
        exec(self.patched_fixture(), namespace)
        scan = namespace["getPEFileUsedDllNames"]
        with tempfile.TemporaryDirectory() as directory:
            binary = Path(directory) / "library.dll"
            binary.write_bytes(b"fixture")
            first = scan(binary)
            self.assertEqual(first, {"normal.dll", "delayed.dll"})
            first.clear()
            self.assertEqual(scan(binary), {"normal.dll", "delayed.dll"})
            reader.assert_called_once_with(os.path.normcase(str(binary)), fast_load=True)
            self.assertEqual(pe.parse_data_directories.call_count, 2)
            binary.write_bytes(b"replacement binary")
            self.assertEqual(scan(binary), {"normal.dll", "delayed.dll"})
            self.assertEqual(reader.call_count, 2)

    def test_reapplication_verifies_the_patch_and_rejects_changed_code(self):
        source = self.patched_fixture()
        block = source.split(patch_nuitka.BEGIN, 1)[1].split(patch_nuitka.END, 1)[0]
        with patch.object(patch_nuitka, "PATCH_DIGEST", patch_nuitka.ast_digest(block)):
            self.assertEqual(patch_nuitka.patch_source(source), source)
            with self.assertRaisesRegex(RuntimeError, "patch has changed"):
                patch_nuitka.patch_source(source.replace("fast_load=True", "fast_load=False"))
        with self.assertRaisesRegex(RuntimeError, "differs from the reviewed"):
            patch_nuitka.patch_source(SCANNER)


if __name__ == "__main__":
    unittest.main()
