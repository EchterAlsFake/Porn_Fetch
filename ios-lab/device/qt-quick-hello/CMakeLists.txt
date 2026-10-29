cmake_minimum_required(VERSION 3.22)
project(QtQuickPhoneHello LANGUAGES CXX)
find_package(Qt6 6.12 REQUIRED COMPONENTS Quick QuickControls2)
qt_standard_project_setup(REQUIRES 6.12)
qt_add_executable(QtQuickPhoneHello MACOSX_BUNDLE main.cpp)
qt_add_qml_module(QtQuickPhoneHello URI PhoneHello VERSION 1.0 QML_FILES Main.qml)
target_link_libraries(QtQuickPhoneHello PRIVATE Qt6::Quick Qt6::QuickControls2)
set_target_properties(QtQuickPhoneHello PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER local.asuna.QtQuickPhoneHello
    MACOSX_BUNDLE_BUNDLE_NAME QtQuickPhoneHello
    MACOSX_BUNDLE_BUNDLE_VERSION 1
    MACOSX_BUNDLE_SHORT_VERSION_STRING 1.0
    XCODE_ATTRIBUTE_CODE_SIGNING_ALLOWED NO)
