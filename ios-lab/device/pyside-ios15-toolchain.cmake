# Qt for Python 6.12 with the already-tested official CPython iOS framework.
include("/Users/asuna/ios-lab/device/qt-ios15/lib/cmake/Qt6/qt.toolchain.cmake")
set(CMAKE_SYSTEM_PROCESSOR arm64)
set(CMAKE_OSX_SYSROOT iphoneos)
set(CMAKE_OSX_ARCHITECTURES arm64)
set(CMAKE_OSX_DEPLOYMENT_TARGET "15.0" CACHE STRING "" FORCE)
set(BUILD_SHARED_LIBS OFF CACHE BOOL "iOS static bindings" FORCE)
set(_PYTHON_SLICE "/Users/asuna/.pyside6_ios/Python-iOS/3.15.0rc2/Python.xcframework/ios-arm64")
set(Python_INCLUDE_DIR "${_PYTHON_SLICE}/include/python3.15" CACHE PATH "" FORCE)
set(Python_LIBRARY "${_PYTHON_SLICE}/lib/libpython3.15.dylib" CACHE FILEPATH "" FORCE)
set(PYTHON_EXECUTABLE "/Users/asuna/ios-lab/device/build-venv/bin/python" CACHE FILEPATH "")
set(Python_SOABI "cpython-315-iphoneos" CACHE STRING "")
# The official host generator links clang statically. Its wrapper needs only
# the bundled host Qt libraries; no target or separate LLVM SDK is needed.
set(SHIBOKEN_WRAPPER_HOST_QT_LIB_PATH "/Users/asuna/ios-lab/.venv/lib/python3.13/site-packages/shiboken6_generator/Qt/lib" CACHE PATH "")
set(SHIBOKEN_WRAPPER_HOST_CLANG_LIB_PATH "/Users/asuna/ios-lab/.venv/lib/python3.13/site-packages/shiboken6_generator/Qt/lib" CACHE PATH "")
