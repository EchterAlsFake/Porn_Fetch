#import <UIKit/UIKit.h>
#import <QuartzCore/CAMetalLayer.h>
#import <Metal/Metal.h>
#import <OpenGLES/EAGL.h>
#include <QJsonArray>
#include <QJsonObject>
#include <QString>
#include <cstdio>

static QString className(id value) { return QString::fromNSString(NSStringFromClass([value class])); }
static QJsonObject describeView(UIView *view, int depth)
{
    QJsonObject result{{"class", className(view)}, {"frame", QString::fromNSString(NSStringFromCGRect(view.frame))},
                       {"hidden", bool(view.hidden)}, {"layer", className(view.layer)}};
    if (depth > 0) {
        QJsonArray children;
        for (UIView *child in view.subviews)
            children.append(describeView(child, depth - 1));
        result["children"] = children;
    }
    return result;
}
void configurePhoneDiagnostics()
{
    NSString *documents = [NSHomeDirectory() stringByAppendingPathComponent:@"Documents"];
    [[NSFileManager defaultManager] createDirectoryAtPath:documents withIntermediateDirectories:YES attributes:nil error:nil];
    freopen([[documents stringByAppendingPathComponent:@"qt-phone-runtime.log"] UTF8String], "w", stderr);
    setenv("QT_LOGGING_RULES", "qt.qpa.*=true;qt.rhi.*=true;qt.widgets.painting=true", 1);
}
QJsonObject phoneWindowState(quintptr viewId)
{
    UIView *view = reinterpret_cast<UIView *>(viewId);
    static id<MTLDevice> metalDevice = MTLCreateSystemDefaultDevice();
    static EAGLContext *glesContext = [[EAGLContext alloc] initWithAPI:kEAGLRenderingAPIOpenGLES3];
    QJsonArray scenes;
    for (UIScene *scene in UIApplication.sharedApplication.connectedScenes) {
        QJsonObject item{{"class", className(scene)}, {"delegate", className(scene.delegate)},
                         {"activation_state", int(scene.activationState)}};
        if ([scene isKindOfClass:UIWindowScene.class]) {
            QJsonArray windows;
            for (UIWindow *window in ((UIWindowScene *)scene).windows) {
                auto windowInfo = describeView(window, 4);
                windowInfo["key_window"] = bool(window.keyWindow);
                windowInfo["root_controller"] = className(window.rootViewController);
                windows.append(windowInfo);
            }
            item["windows"] = windows;
        }
        scenes.append(item);
    }
    return {{"connected_scenes", scenes}, {"qt_view", describeView(view, 1)},
            {"metal_device", QString::fromNSString(metalDevice.name)},
            {"gles3_context_available", bool(glesContext)},
            {"qt_view_has_superview", bool(view.superview)}, {"qt_view_has_window", bool(view.window)}};
}
