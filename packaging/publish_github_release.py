"""Publish immutable GitHub assets, resuming an interrupted draft or upload."""
import argparse
import hashlib
import json
import os
import subprocess
import tempfile
from pathlib import Path


def gh(*args: str) -> str:
    return subprocess.check_output(['gh', *args], text=True)


def publish(assets: Path, version: str, commit: str, channel: str, notes: Path) -> None:
    tag = f'v{version}'
    tag_ref = f'refs/tags/{tag}'
    repository = os.environ['GITHUB_REPOSITORY']
    def lookup(endpoint: str):
        result = subprocess.run(['gh', 'api', f'repos/{repository}/{endpoint}'], capture_output=True, text=True)
        if result.returncode:
            if 'HTTP 404' in result.stderr:
                return None
            raise RuntimeError(result.stderr)
        return json.loads(result.stdout)

    if lookup(f'git/ref/tags/{tag}') is None:
        gh('api', f'repos/{repository}/git/refs', '-X', 'POST', '-f', f'ref={tag_ref}', '-f', f'sha={commit}')
    actual_commit = gh('api', f'repos/{repository}/commits/{tag_ref}', '--jq', '.sha').strip()
    if actual_commit != commit:
        raise ValueError('Existing release tag points to a different commit')
    releases = lookup(f'releases/tags/{tag}')
    if releases is None:
        gh('release', 'create', tag, '--draft', '--verify-tag', '--title', f'Porn Fetch {version}',
           '--notes-file', str(notes), f'--prerelease={str(channel == "beta").lower()}')
    if releases is not None and releases['prerelease'] != (channel == 'beta'):
        raise ValueError('Existing release has a different channel')
    existing = {item['name'] for item in (releases or {}).get('assets', [])}
    files = sorted(path for path in assets.iterdir() if path.is_file())
    if not files:
        raise ValueError('No release assets')
    with tempfile.TemporaryDirectory(prefix='release-verify-') as directory:
        for path in files:
            if path.name in existing:
                gh('release', 'download', tag, '--pattern', path.name, '--dir', directory)
                with path.open('rb') as source, (Path(directory) / path.name).open('rb') as remote:
                    if hashlib.file_digest(source, 'sha256').digest() != hashlib.file_digest(remote, 'sha256').digest():
                        raise ValueError(f'Existing release asset differs: {path.name}')
            else:
                gh('release', 'upload', tag, str(path))
    gh('release', 'edit', tag, '--draft=false')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--assets', type=Path, required=True)
    parser.add_argument('--version', required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--channel', choices=('stable', 'beta'), required=True)
    parser.add_argument('--notes', type=Path, required=True)
    args = parser.parse_args()
    publish(args.assets, args.version, args.commit, args.channel, args.notes)
