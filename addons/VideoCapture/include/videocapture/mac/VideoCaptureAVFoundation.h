/*
  
  VideoCaptureAVFoundation
  -------------------------
  Basic webcam grabber based on the examples provided by apple and their reference.
  This is still work in progress and we need to check if all memory management is 
  handled correctly. 

  Also, something silly happens when you ask for a grabber with a certain pixel format 
  and resolution which is not supported. The VideoCaptureInput device will try to get the
  best format you ask for, but this might be in a different format. 
  
  So if you want to capture in YUV, it might actually end up capturing using mpeg (code: 1bmd, or dmb1)
  but the AVCaptureVideoOutput seems to convert this format again. This is something I need to fix, or
  at least show some verbose info when this happens. (May 2013)

  --
  Update 2013.12.10:
  Added an `in_codec` to the VideoCaptureSettings so you can use a specific codec and 
  ask mac to decode it into `in_pixel_format` for you.
  
  --


  TODO: - this code creates nice localized names for video types: 
          https://gist.github.com/roxlu/f2168a49cc5693193826
 
        - figure out this problem I posted on stackoverflow:
          http://stackoverflow.com/questions/16619068/capture-from-webcam-using-default-uncompressed-pixel-format-using-avfoundation
        

 */
#undef DEBUG /* resulted in wierd errors with roxlu lib */
#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>
#import <CoreMedia/CMBufferQueue.h>
#include <videocapture/Types.h>
#include <vector>

#define ERR_CM_DEVICE_NOT_FOUND "We couldn't find the given input device\n"
#define ERR_CM_FORMAT_NOT_FOUND "Cannot open device because we cannot find the format/size/fps you want\n"
#define ERR_CM_CAPTURE_DEVICE "Cannot initialize AVCaptureDeviceInput\n"
#define ERR_CM_ALLOC_SESSION "Cannot allocate an AVCaptureSession\n"
#define ERR_CM_SESSION_INPUT "Cannot add input to current session; session needs to be configured.\n"
#define ERR_CM_PIX_FMT "The pixelformat is not supported by AVCaptureDeviceOutput. This does not mean that the webcam doesn't support this format, just the Mac AVCaptureVideoDataOutput not\n"
#define ERR_CM_OUTPUT "Cannot add output to current session; sessions needs to be configured.\n"

@interface VideoCaptureAVFoundation : NSObject<AVCaptureVideoDataOutputSampleBufferDelegate> {
  AVCaptureSession* session;                             /* Manages the state of the input device */
  AVCaptureDeviceInput* input;                           /* Concrete instance of `AVDeviceInput`,  represents the input device (webcam) */
  AVCaptureVideoDataOutput* output;                      /* Concrete instance of `AVDeviceOutput`, used to get the video frames */
  videocapture_frame_cb cb_frame;                        /* Gets called when we receive a new frame */
  void* cb_user;                                         /* User data that's will be passed into `cb_frame()` */
}

- (int) listDevices;

- (int) openDevice: (int) device 
         withWidth: (int) w 
         andHeight: (int) h 
         andFormat: (VideoCaptureFormat) fmt
          andCodec: (VideoCaptureFormat) codec
      andFrameRate: (float) fps;                                                                 /* values like: 30.00, 29.97, 20.00, 5.00 etc.. are valid */

- (int) closeDevice;

- (void) captureOutput: (AVCaptureOutput*) captureOutput
 didOutputSampleBuffer: (CMSampleBufferRef) sampleBuffer
        fromConnection: (AVCaptureConnection*) connection;

- (int) captureStart;

- (int) captureStop;

- (void) setFrameCallback: (videocapture_frame_cb) frameCB 
                     user: (void*) frameUser;

- (AVCaptureDevice*) getCaptureDevice: (int) device;


- (NSString* const) widthHeightToCaptureSessionPreset:(int) w 
                                            andHeight:(int) h;

- (NSString*) pixelFormatToString: (CMPixelFormatType) fmt;

- (int) videoCapturePixelFormatToAVFoundationPixelFormat: (VideoCaptureFormat) fmt;

- (int) avFoundationPixelFormatToVideoCaptureFormat: (int) fmt;

- (NSString*) getPixelFormatString: (CMPixelFormatType) fmt;

- (int) getCapabilities: (std::vector<VideoCaptureCapability>&) result
              forDevice: (int) device;

- (int) isPixelFormatSupportedByCaptureVideoDataOutput: (AVCaptureVideoDataOutput*) o
                                           pixelFormat: (VideoCaptureFormat) fmt;

- (void) printSupportedPixelFormatsByVideoDataOutput: (AVCaptureVideoDataOutput*) o;          /* note: this are not the supported pixel formats of the webcam. Mac uses another object where you define the output format type. */
- (void) printSupportedVideoCodecFormatsByVideoDataOutput: (AVCaptureVideoDataOutput*) o;     /* prints ths video codecs that are supported by the data-output (not necessarily of the dvice) */

@end
