"""Speed up Nuitka's Windows ARM64 PE dependency scanner in the active environment.

Only the reviewed Nuitka 4.3.4 function is modified. Keep normal and delayed
imports, skip unrelated PE directories, and cache import names for unchanged
files during this compiler process. DLL resolution still runs for each context.
"""
from __future__ import annotations

import ast
import hashlib
import importlib.util
import os
import sys
import tempfile
from pathlib import Path

SOURCE_DIGEST = "ee7a5bdb44da49c5fa1415d42909100b9e3110e8a2d98fa7f98afa7151af739f"
PATCH_DIGEST = "409dd9f85a23029a01d6697ce830f786bed231fc2ad3b6791d7cd51f6de54df9"
BEGIN = "# BEGIN pornfetch-nuitka-pe-imports-v1\n"
END = "# END pornfetch-nuitka-pe-imports-v1\n"
WRAPPER = '''
_pornfetch_pe_imports = {}


def getPEFileUsedDllNames(filename):
    filename = os.path.normcase(os.path.abspath(filename))
    info = os.stat(filename)
    signature = (info.st_size, info.st_mtime_ns)
    cached = _pornfetch_pe_imports.get(filename)
    if cached is None or cached[0] != signature:
        names = _pornfetchReadPEImports(filename)
        cached = (signature, tuple(names) if names is not None else None)
        _pornfetch_pe_imports[filename] = cached
    # Return a fresh collection so callers cannot change cached names.
    return OrderedSet(cached[1]) if cached[1] is not None else None
'''


def ast_digest(source: str) -> str:
    return hashlib.sha256(ast.dump(ast.parse(source), show_empty=True).encode()).hexdigest()


def patch_source(source: str) -> str:
    if BEGIN in source:
        block = source.split(BEGIN, 1)[1].split(END, 1)[0]
        if source.count(BEGIN) != 1 or source.count(END) != 1 or ast_digest(block) != PATCH_DIGEST:
            raise RuntimeError("The installed Nuitka PE scanner patch has changed; review it before compiling.")
        return source
    functions = [node for node in ast.parse(source).body
                 if isinstance(node, ast.FunctionDef) and node.name == "getPEFileUsedDllNames"]
    if len(functions) != 1:
        raise RuntimeError("Cannot locate Nuitka's PE scanner; review the installed Nuitka before compiling.")
    function = functions[0]
    original = ast.get_source_segment(source, function)
    if function.decorator_list or original is None or ast_digest(original) != SOURCE_DIGEST:
        raise RuntimeError("Nuitka's PE scanner differs from the reviewed 4.3.4 implementation. "
                           "Review scripts/patch_nuitka.py for this Nuitka version before compiling.")
    reader = original.replace("def getPEFileUsedDllNames(", "def _pornfetchReadPEImports(", 1).replace(
        "pefile.PE(filename)", "pefile.PE(filename, fast_load=True)", 1)
    replacement = BEGIN + reader + "\n\n" + WRAPPER + END
    lines = source.splitlines(keepends=True)
    updated = "".join(lines[:function.lineno - 1]) + replacement + "".join(lines[function.end_lineno:])
    compile(updated, "Nuitka/utils/SharedLibraries.py", "exec")
    return updated


def patch_installed_nuitka() -> None:
    spec = importlib.util.find_spec("nuitka")
    if spec is None or spec.origin is None:
        raise RuntimeError("Install the desktop-build extra before preparing a Windows ARM64 GUI build.")
    path = Path(spec.origin).resolve().parent / "utils/SharedLibraries.py"
    if not path.is_relative_to(Path(sys.prefix).resolve()):
        raise RuntimeError(f"Refusing to modify Nuitka outside the active Python environment: {path}")
    source = path.read_text(encoding="utf-8")
    updated = patch_source(source)
    if updated == source:
        print(f"Nuitka ARM64 PE import cache verified: {path}", flush=True)
        return
    # Replace rather than editing in place: uv may have hardlinked this file to
    # its package cache. Never change other environments or a partially written file.
    with tempfile.NamedTemporaryFile(dir=path.parent, suffix=".py", delete=False) as stream:
        temporary = Path(stream.name)
        stream.write(updated.encode("utf-8"))
    try:
        temporary.chmod(path.stat().st_mode)
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)
    print(f"Nuitka ARM64 PE import cache applied: {path}", flush=True)


if __name__ == "__main__":
    patch_installed_nuitka()
