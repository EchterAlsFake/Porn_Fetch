# Intel iOS simulator recipes

The real Porn Fetch backend and mobile QML interface ran in the iOS 26.3 simulator
on the original Intel macOS VM. Native dependency probes and a complete decode
of a user download passed. Reports are in `../results/`.

Use the [simulator build instructions](../../docs/ios/BUILDING.md#intel-simulator)
after restoring the lab inputs. This target uses official Qt/PySide wheels with
an iOS 18 minimum and embedded Python 3.15.0rc2. It is separate from the patched
arm64/iOS 15 device kit.

The launcher selects OpenGL with the basic render loop for the tested VM's CPU
renderer. The phone uses Metal instead. The device FFmpeg adapter has not been
integrated into this simulator target; its successful download produced an MP4
that did not need local remuxing.
