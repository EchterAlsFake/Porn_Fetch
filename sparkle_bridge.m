// sparkle_bridge.m
// Build as a .dylib and place into MyApp.app/Contents/Frameworks/

#import <Foundation/Foundation.h>
#import <AppKit/AppKit.h>
#import <Sparkle/Sparkle.h>

@interface SparkleBridgeDelegate : NSObject <SPUUpdaterDelegate>
@property (nonatomic, copy) NSString *feedURLString;
@end

@implementation SparkleBridgeDelegate
- (nullable NSString *)feedURLStringForUpdater:(SPUUpdater *)updater
{
    // Return nil to use SUFeedURL from Info.plist.
    // Return a string here to override dynamically.
    return self.feedURLString;
}
@end

static SPUStandardUpdaterController *gUpdaterController = nil;
static SparkleBridgeDelegate *gDelegate = nil;

// Helper: ensure all Sparkle API usage happens on the main thread
static void run_on_main(void (^block)(void)) {
    if ([NSThread isMainThread]) {
        block();
    } else {
        dispatch_sync(dispatch_get_main_queue(), block);
    }
}

__attribute__((visibility("default")))
void sparkle_start_updater(const char *feed_url_utf8)
{
    run_on_main(^{
        if (gUpdaterController != nil) {
            return;
        }

        gDelegate = [SparkleBridgeDelegate new];

        if (feed_url_utf8 != NULL && strlen(feed_url_utf8) > 0) {
            gDelegate.feedURLString = [NSString stringWithUTF8String:feed_url_utf8];
        } else {
            // Use SUFeedURL from Info.plist (delegate returns nil)
            gDelegate.feedURLString = nil;
        }

        // Create controller and start updater immediately.
        // This uses Sparkle’s standard UI and targets the main bundle.
        gUpdaterController = [[SPUStandardUpdaterController alloc]
            initWithStartingUpdater:YES
                    updaterDelegate:gDelegate
                  userDriverDelegate:nil];
    });
}

__attribute__((visibility("default")))
void sparkle_check_for_updates(void)
{
    run_on_main(^{
        if (gUpdaterController == nil) {
            // If you forgot to call sparkle_start_updater(), start with Info.plist config.
            sparkle_start_updater(NULL);
        }
        [gUpdaterController checkForUpdates:nil];
    });
}

__attribute__((visibility("default")))
void sparkle_check_for_updates_in_background(void)
{
    run_on_main(^{
        if (gUpdaterController == nil) {
            sparkle_start_updater(NULL);
        }

        // Note: Sparkle already schedules background checks (default ~24h)
        // if automatic checks are enabled.
        // Calling this manually can interfere with the scheduler if used incorrectly.
        // See Sparkle docs.
        [gUpdaterController.updater checkForUpdatesInBackground];
    });
}

__attribute__((visibility("default")))
int sparkle_can_check_for_updates(void)
{
    __block int result = 0;
    run_on_main(^{
        if (gUpdaterController == nil) {
            sparkle_start_updater(NULL);
        }
        result = gUpdaterController.updater.canCheckForUpdates ? 1 : 0;
    });
    return result;
}
