// Included by the generated iOS entry point. No Python ABI or external dependency.
#import <Foundation/Foundation.h>
#import <UIKit/UIKit.h>
#import <UserNotifications/UserNotifications.h>
#include <QCoreApplication>
#include <QFileSystemWatcher>
#include <QTimer>

static NSString *notificationDirectory()
{
    NSString *cache = NSSearchPathForDirectoriesInDomains(NSCachesDirectory, NSUserDomainMask, YES).firstObject;
    return [cache stringByAppendingPathComponent:@"PornFetchNotifications"];
}

static void publishNotificationStatus()
{
    [[UNUserNotificationCenter currentNotificationCenter] getNotificationSettingsWithCompletionHandler:
        ^(UNNotificationSettings *settings) {
            NSString *state = @"denied";
            if (settings.authorizationStatus == UNAuthorizationStatusAuthorized
                    || settings.authorizationStatus == UNAuthorizationStatusProvisional)
                state = @"allowed";
            else if (settings.authorizationStatus == UNAuthorizationStatusNotDetermined)
                state = @"pending";
            NSData *data = [NSJSONSerialization dataWithJSONObject:@{@"state": state} options:0 error:nil];
            [data writeToFile:[notificationDirectory() stringByAppendingPathComponent:@"notifications-state.json"]
                options:NSDataWritingAtomic error:nil];
        }];
}

static void consumeNotificationCommand()
{
    @autoreleasepool {
        NSString *path = [notificationDirectory() stringByAppendingPathComponent:@"notifications-request.json"];
        NSData *data = [NSData dataWithContentsOfFile:path];
        if (!data) return;
        NSDictionary *command = [NSJSONSerialization JSONObjectWithData:data options:0 error:nil];
        [[NSFileManager defaultManager] removeItemAtPath:path error:nil];
        if (![command isKindOfClass:[NSDictionary class]]) return;
        NSString *action = command[@"action"];
        UNUserNotificationCenter *center = [UNUserNotificationCenter currentNotificationCenter];
        if ([action isEqualToString:@"enable"]) {
            [center getNotificationSettingsWithCompletionHandler:^(UNNotificationSettings *settings) {
                if (settings.authorizationStatus == UNAuthorizationStatusNotDetermined) {
                    [center requestAuthorizationWithOptions:UNAuthorizationOptionAlert
                        completionHandler:^(BOOL granted, NSError *error) { publishNotificationStatus(); }];
                } else {
                    publishNotificationStatus();
                }
            }];
        } else if ([action isEqualToString:@"settings"]) {
            [[UIApplication sharedApplication] openURL:[NSURL URLWithString:UIApplicationOpenSettingsURLString]
                options:@{} completionHandler:nil];
        } else if ([action isEqualToString:@"disable"]) {
            [center removePendingNotificationRequestsWithIdentifiers:@[@"download-results"]];
            [center removeDeliveredNotificationsWithIdentifiers:@[@"download-results"]];
        } else if ([action isEqualToString:@"notify"]) {
            NSString *message = command[@"message"];
            NSString *title = command[@"title"];
            if (![message isKindOfClass:[NSString class]] || ![title isKindOfClass:[NSString class]]) return;
            [center getNotificationSettingsWithCompletionHandler:^(UNNotificationSettings *settings) {
                if (settings.authorizationStatus != UNAuthorizationStatusAuthorized
                        && settings.authorizationStatus != UNAuthorizationStatusProvisional) return;
                UNMutableNotificationContent *content = [UNMutableNotificationContent new];
                content.title = title;
                content.body = message;
                content.threadIdentifier = @"download-results";
                UNNotificationRequest *request = [UNNotificationRequest requestWithIdentifier:@"download-results"
                    content:content trigger:nil];
                [center addNotificationRequest:request withCompletionHandler:^(NSError *error) {
                    publishNotificationStatus();
                }];
#if !__has_feature(objc_arc)
                [content release];
#endif
            }];
        }
        publishNotificationStatus();
    }
}

static void startNotificationBridge()
{
    @autoreleasepool {
        [[NSFileManager defaultManager] createDirectoryAtPath:notificationDirectory()
            withIntermediateDirectories:YES attributes:nil error:nil];
        auto *watcher = new QFileSystemWatcher(QCoreApplication::instance());
        watcher->addPath(QString::fromUtf8(notificationDirectory().UTF8String));
        QObject::connect(watcher, &QFileSystemWatcher::directoryChanged, watcher,
            [](const QString &) { consumeNotificationCommand(); });
        QTimer::singleShot(0, watcher, [] { consumeNotificationCommand(); publishNotificationStatus(); });
    }
}
Q_COREAPP_STARTUP_FUNCTION(startNotificationBridge)
