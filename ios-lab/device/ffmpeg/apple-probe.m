#define PY_SSIZE_T_CLEAN
#include <Python.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreVideo/CoreVideo.h>
#import <AudioToolbox/AudioToolbox.h>

PyObject *ios_media_probe(PyObject *self, PyObject *args) {
    const char *path;
    if (!PyArg_ParseTuple(args, "s", &path)) return NULL;
    @autoreleasepool {
        AVURLAsset *asset = [AVURLAsset URLAssetWithURL:[NSURL fileURLWithPath:@(path)]
            options:@{AVURLAssetPreferPreciseDurationAndTimingKey:@YES}];
        NSMutableArray *tracks = [NSMutableArray array];
        NSMutableDictionary *decoded = [NSMutableDictionary dictionary];
        for (AVAssetTrack *track in asset.tracks) {
            [tracks addObject:@{@"type":track.mediaType, @"width":@(track.naturalSize.width),
                @"height":@(track.naturalSize.height), @"frame_rate":@(track.nominalFrameRate)}];
            BOOL video = [track.mediaType isEqualToString:AVMediaTypeVideo];
            BOOL audio = [track.mediaType isEqualToString:AVMediaTypeAudio];
            if ((video || audio) && !decoded[track.mediaType]) {
                NSError *error = nil;
                AVAssetReader *reader = [[AVAssetReader alloc] initWithAsset:asset error:&error];
                NSDictionary *settings = video
                    ? @{(id)kCVPixelBufferPixelFormatTypeKey:@(kCVPixelFormatType_420YpCbCr8BiPlanarVideoRange)}
                    : @{AVFormatIDKey:@(kAudioFormatLinearPCM)};
                AVAssetReaderTrackOutput *output = [[AVAssetReaderTrackOutput alloc]
                    initWithTrack:track outputSettings:settings];
                BOOL success = NO;
                if ([reader canAddOutput:output]) {
                    [reader addOutput:output];
                    if ([reader startReading]) {
                        CMSampleBufferRef sample = [output copyNextSampleBuffer];
                        success = sample && CMSampleBufferGetNumSamples(sample) > 0;
                        if (sample) CFRelease(sample);
                    }
                }
                decoded[track.mediaType] = @(success);
                if (reader.error) decoded[[track.mediaType stringByAppendingString:@"_error"]] = reader.error.localizedDescription;
                [reader cancelReading];
                [output release];
                [reader release];
            }
        }
        double duration = CMTimeGetSeconds(asset.duration);
        NSDictionary *result = @{@"playable":@(asset.playable), @"readable":@(asset.readable),
            @"duration_seconds":@(isfinite(duration) ? duration : -1), @"tracks":tracks, @"decoded_samples":decoded};
        NSData *json = [NSJSONSerialization dataWithJSONObject:result options:0 error:nil];
        return PyUnicode_DecodeUTF8(json.bytes, json.length, "strict");
    }
}
