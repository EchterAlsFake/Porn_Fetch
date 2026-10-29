#import <UIKit/UIKit.h>
#include <Python/Python.h>

static void startPython(void) {
    NSString *root = NSBundle.mainBundle.resourcePath;
    NSString *home = [root stringByAppendingPathComponent:@"python"];
    NSString *stdlib = [home stringByAppendingPathComponent:@"lib/python3.15"];
    PyPreConfig pre;
    PyPreConfig_InitIsolatedConfig(&pre);
    pre.utf8_mode = 1;
    PyStatus status = Py_PreInitialize(&pre);
    if (PyStatus_Exception(status)) Py_ExitStatusException(status);
    PyConfig config;
    PyConfig_InitIsolatedConfig(&config);
    config.buffered_stdio = 0;
    config.write_bytecode = 0;
    config.install_signal_handlers = 0;
    config.home = Py_DecodeLocale(home.UTF8String, NULL);
    config.module_search_paths_set = 1;
    wchar_t *path = Py_DecodeLocale(stdlib.UTF8String, NULL);
    PyWideStringList_Append(&config.module_search_paths, path);
    PyMem_RawFree(path);
    for (NSString *extra in @[[stdlib stringByAppendingPathComponent:@"lib-dynload"],
                              [root stringByAppendingPathComponent:@"packages"]]) {
        path = Py_DecodeLocale(extra.UTF8String, NULL);
        PyWideStringList_Append(&config.module_search_paths, path);
        PyMem_RawFree(path);
    }
    status = Py_InitializeFromConfig(&config);
    PyConfig_Clear(&config);
    if (PyStatus_Exception(status)) Py_ExitStatusException(status);
    int result = PyRun_SimpleString(
        "import json, os, sys\n"
        "result = {'version': sys.version, 'platform': sys.platform, 'sum_squares': sum(i*i for i in range(100))}\n"
        "assert result['sum_squares'] == 328350\n"
        "directory = os.path.expanduser('~/Documents')\n"
        "os.makedirs(directory, exist_ok=True)\n"
        "with open(os.path.join(directory, 'python-native-result.json'), 'w') as f: json.dump(result, f)\n"
        "print('PYTHON_NATIVE_DEVICE_PASS', json.dumps(result), flush=True)\n"
    );
    if (result != 0) abort();
    NSString *probe = [root stringByAppendingPathComponent:@"probe.py"];
    if ([[NSFileManager defaultManager] fileExistsAtPath:probe]) {
        FILE *file = fopen(probe.UTF8String, "r");
        if (!file || PyRun_SimpleFileEx(file, probe.UTF8String, 1) != 0) abort();
    }
}

@interface PythonDelegate : UIResponder <UIApplicationDelegate>
@property (strong, nonatomic) UIWindow *window;
@end
@implementation PythonDelegate
- (BOOL)application:(UIApplication *)application didFinishLaunchingWithOptions:(NSDictionary *)options {
    self.window = [[UIWindow alloc] initWithFrame:UIScreen.mainScreen.bounds];
    UIViewController *controller = [UIViewController new];
    controller.view.backgroundColor = UIColor.systemBackgroundColor;
    UILabel *label = [UILabel new];
    label.text = @"Hello Python 3.15!\nRunning on the real iPhone.";
    if ([[NSFileManager defaultManager] fileExistsAtPath:[NSBundle.mainBundle.resourcePath stringByAppendingPathComponent:@"probe.py"]])
        label.text = @"Python native module checks\nResults saved in Documents.";
    label.numberOfLines = 0;
    label.textAlignment = NSTextAlignmentCenter;
    label.textColor = UIColor.labelColor;
    label.font = [UIFont systemFontOfSize:24];
    label.translatesAutoresizingMaskIntoConstraints = NO;
    [controller.view addSubview:label];
    [NSLayoutConstraint activateConstraints:@[
        [label.centerXAnchor constraintEqualToAnchor:controller.view.centerXAnchor],
        [label.centerYAnchor constraintEqualToAnchor:controller.view.centerYAnchor]
    ]];
    self.window.rootViewController = controller;
    [self.window makeKeyAndVisible];
    return YES;
}
@end
int main(int argc, char **argv) {
    @autoreleasepool {
        startPython();
        return UIApplicationMain(argc, argv, nil, NSStringFromClass(PythonDelegate.class));
    }
}
