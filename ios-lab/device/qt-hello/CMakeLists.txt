cmake_minimum_required(VERSION 3.22)
project(QtPhoneHello LANGUAGES CXX OBJCXX)
find_package(Qt6 6.12 REQUIRED COMPONENTS Widgets)
qt_standard_project_setup()
qt_add_executable(QtPhoneHello MACOSX_BUNDLE main.cpp ios-diagnostics.mm)
target_link_libraries(QtPhoneHello PRIVATE Qt6::Widgets)
set_target_properties(QtPhoneHello PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER local.asuna.QtPhoneHello
    MACOSX_BUNDLE_BUNDLE_NAME QtPhoneHello
    MACOSX_BUNDLE_BUNDLE_VERSION 1
    MACOSX_BUNDLE_SHORT_VERSION_STRING 1.0
    XCODE_ATTRIBUTE_CODE_SIGNING_ALLOWED NO)
