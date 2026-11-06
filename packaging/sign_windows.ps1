<#
Sign release PE files with Certum SimplySign and verify them with Windows trust APIs.
Credentials are read by ssign from CERTUM_EMAIL and CERTUM_OTP only.
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)] [string[]] $Paths,
    [switch] $Force,
    [switch] $VerifyOnly
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

if (!$IsWindows) { throw 'Authenticode verification requires Windows' }
if (!$VerifyOnly -and (!$env:CERTUM_EMAIL -or !$env:CERTUM_OTP)) {
    throw 'The signing environment must provide CERTUM_EMAIL and CERTUM_OTP (the TOTP seed)'
}

$files = @(
    foreach ($path in $Paths) {
        $item = Get-Item -LiteralPath $path
        if ($item.PSIsContainer) { Get-ChildItem -LiteralPath $path -File -Recurse }
        else { $item }
    }
) | Where-Object { $_.Extension.ToLowerInvariant() -in '.exe', '.dll', '.pyd', '.sys' } |
    Sort-Object -Property FullName -Unique
if (!$files) { throw 'No Windows PE files found in the requested signing paths' }

$pending = @(
    foreach ($file in $files) {
        $signature = Get-AuthenticodeSignature -LiteralPath $file.FullName
        if ($signature.Status -eq 'Valid' -and (!$Force -or $VerifyOnly -or $file.Extension -eq '.sys')) {
            continue
        } elseif (!$VerifyOnly -and $file.Extension -ne '.sys' -and ($Force -or $signature.Status -eq 'NotSigned')) {
            $file.FullName
        } else {
            throw "Untrusted signature on $($file.FullName): $($signature.Status) ($($signature.StatusMessage))"
        }
    }
)

# Small batches stay below Windows' command-line limit. ssign reuses its session.
for ($offset = 0; $offset -lt $pending.Count; $offset += 20) {
    $batch = @($pending[$offset..([Math]::Min($offset + 19, $pending.Count - 1))])
    for ($attempt = 1; $attempt -le 5; $attempt++) {
        & ssign --timestamp-url 'http://time.certum.pl/' --name 'Porn Fetch' --url 'https://pornfetch.to' @batch 2>&1 |
            Tee-Object -Variable output | Out-Host
        if ($LASTEXITCODE -eq 0) { break }
        # Certum accepts an OTP only once. Concurrent matrix jobs may log in in
        # the same 30-second window; retry login in a fresh window with jitter.
        if ($attempt -eq 5 -or ($output -join "`n") -notmatch 'login|no authorization code') {
            throw "ssign failed (exit $LASTEXITCODE)"
        }
        Write-Host "Certum login failed; retrying in a fresh OTP window (attempt $attempt/5)."
        Start-Sleep -Seconds (31 + (Get-Random -Minimum 0 -Maximum 10))
    }
}

foreach ($file in $files) {
    $signature = Get-AuthenticodeSignature -LiteralPath $file.FullName
    if ($signature.Status -ne 'Valid') {
        throw "Signature verification failed for $($file.FullName): $($signature.Status)"
    }
    if ($file.FullName -in $pending -and !$signature.TimeStamperCertificate) {
        throw "RFC3161 timestamp missing from $($file.FullName)"
    }
    Write-Host "Verified $($file.FullName) [$($signature.SignerCertificate.Subject)]"
    if (!$VerifyOnly -and ($file.Extension -eq '.exe' -or (Test-Path -LiteralPath "$($file.FullName).sha256"))) {
        $digest = (Get-FileHash -LiteralPath $file.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        [System.IO.File]::WriteAllText("$($file.FullName).sha256", "$digest  $($file.Name)`n")
    }
}
