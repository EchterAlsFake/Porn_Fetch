# Physical device recipes

Target verified on 2026-10-28: iPhone 7, arm64, iOS 15.8.8, palera1n rootless.

See the [build guide](../../docs/ios/BUILDING.md) for prerequisites, source build
order, project generation, signing, deployment, and incremental rebuilds.
The [implementation notes](../../docs/ios/ARCHITECTURE.md) explain the Qt patch,
GPU entitlement, framework packaging, FFmpeg integration, and validation scope.

The main path is `prepare-application.py` → `build-application.sh` →
`deploy-app.sh PornFetch`. These require restored or rebuilt dependencies.
`BUILD-REVISIONS.json` records the original inputs; `../results/` contains
selected device and simulator reports.
