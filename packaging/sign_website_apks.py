"""Re-sign downloaded APKs with the GitHub release keystore before publication."""
import base64
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def sign(artifacts: Path) -> None:
    # GitHub can place each downloaded APK inside a directory with the same name.
    apks = sorted(path for path in artifacts.rglob('*.apk') if path.is_file(follow_symlinks=False))
    if not apks:
        return
    required = ('ANDROID_KEYSTORE_BASE64', 'ANDROID_KEYSTORE_PASSWORD', 'ANDROID_KEY_ALIAS', 'ANDROID_KEY_PASSWORD')
    for name in required:
        if not os.environ.get(name):
            raise ValueError(f'Missing publication credential: {name}')
    sdk = Path(os.environ['ANDROID_HOME'])
    tools = sdk / 'build-tools/36.0.0'
    with tempfile.TemporaryDirectory(prefix='apk-publish-') as temporary:
        work = Path(temporary)
        keystore = work / 'release.jks'
        keystore.write_bytes(base64.b64decode(os.environ['ANDROID_KEYSTORE_BASE64'], validate=True))
        keystore.chmod(0o600)
        certificate = subprocess.check_output([
            'keytool', '-exportcert', '-keystore', str(keystore), '-alias', os.environ['ANDROID_KEY_ALIAS'],
            '-storepass:env', 'ANDROID_KEYSTORE_PASSWORD',
        ])
        expected = hashlib.sha256(certificate).hexdigest()

        def signer(path: Path) -> str | None:
            result = subprocess.run([str(tools / 'apksigner'), 'verify', '--print-certs', str(path)],
                                    capture_output=True, text=True)
            if result.returncode:
                return None
            # Newer apksigner versions can print the same certificate per scheme.
            fingerprints = set(re.findall(
                r'^(?:v[0-9.]+ )?signer(?: #\d+)?:? certificate sha-256 digest: ([0-9a-f]{64})$',
                result.stdout.lower(), re.MULTILINE,
            ))
            return fingerprints.pop() if len(fingerprints) == 1 else None

        for apk in apks:
            if signer(apk) == expected:
                continue  # Preserve already-correct release bytes on publication retries.
            aligned, signed = work / 'aligned.apk', work / 'signed.apk'
            subprocess.run([str(tools / 'zipalign'), '-P', '16', '-f', '4', str(apk), str(aligned)], check=True)
            subprocess.run([str(tools / 'apksigner'), 'sign', '--ks', str(keystore),
                            '--ks-key-alias', os.environ['ANDROID_KEY_ALIAS'],
                            '--ks-pass', 'env:ANDROID_KEYSTORE_PASSWORD', '--key-pass', 'env:ANDROID_KEY_PASSWORD',
                            '--out', str(signed), str(aligned)], check=True)
            subprocess.run([str(tools / 'apksigner'), 'verify', '--verbose', str(signed)], check=True)
            if signer(signed) != expected:
                raise ValueError('Signed APK does not match the release keystore certificate')
            apk.write_bytes(signed.read_bytes())
            digest = hashlib.sha256(apk.read_bytes()).hexdigest()
            apk.with_name(apk.name + '.sha256').write_text(f'{digest}  {apk.name}\n')


if __name__ == '__main__':
    sign(Path(sys.argv[1]))
