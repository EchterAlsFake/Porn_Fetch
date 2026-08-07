#import <Foundation/Foundation.h>
#import <AppKit/AppKit.h>
#import <Sparkle/Sparkle.h>

static SPUStandardUpdaterController *gUpdaterController = nil;

static void run_on_main(void (^block)(void))
{
    if ([NSThread isMainThread]) {
        block();
    } else {
        dispatch_sync(dispatch_get_main_queue(), block);
    }
}

__attribute__((visibility("default")))
void sparkle_start_updater(void)
{
    run_on_main(^{
        @autoreleasepool {
            if (gUpdaterController != nil) {
                return;
            }

            gUpdaterController =
                [[SPUStandardUpdaterController alloc]
                    initWithStartingUpdater:YES
                    updaterDelegate:nil
                    userDriverDelegate:nil];
        }
    });
}

__attribute__((visibility("default")))
void sparkle_check_for_updates(void)
{
    run_on_main(^{
        @autoreleasepool {
            if (gUpdaterController == nil) {
                sparkle_start_updater();
            }

            [gUpdaterController checkForUpdates:nil];
        }
    });
}

__attribute__((visibility("default")))
int sparkle_can_check_for_updates(void)
{
    __block int result = 0;

    run_on_main(^{
        @autoreleasepool {
            if (gUpdaterController == nil) {
                sparkle_start_updater();
            }

            result =
                gUpdaterController.updater.canCheckForUpdates
                ? 1
                : 0;
        }
    });

    return result;
}