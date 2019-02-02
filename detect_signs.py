import cv2
#import apriltag
import RPi.GPIO as GPIO
from picamera import PiCamera
from picamera.array import PiRGBArray



####### TO BE TESTED ON PI #######

class DetectSigns:
    def __init__(self, frame_width=640, frame_height=480, servo_x=3, servo_y=5, laser=7, speed_control=1, laser_face_distance=50):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_center_x = frame_width / 2
        self.frame_center_y = frame_height / 2

        self.intersection_pin = 3
        self.stop_sign_pin = 5

        self.classifier_path = "stopsign_classifier.xml"
        self.classifier = cv2.CascadeClassifier(self.classifier_path)
        #self.detector_april = apriltag.Detector()


        self.camera = PiCamera()
        self.camera.resolution = (frame_width, frame_height)
        self.camera.framerate = 32
        self.rawCapture = PiRGBArray(self.camera, size=(frame_width, frame_height))

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.intersection_pin, GPIO.OUT)
        GPIO.setup(self.stop_sign_pin, GPIO.OUT)

        GPIO.output(self.intersection_pin, False)
        GPIO.output(self.stop_sign_pin, False)


    def start(self):
        for frame_temp in self.camera.capture_continuous(self.rawCapture, format='bgr', use_video_port=True):
            x1, x2, y1, y2 = (240, 400, 0, 200)
            frame_temp = frame_temp.array[y1:y2, x1:x2]

            gray_temp = cv2.cvtColor(frame_temp, cv2.COLOR_BGR2GRAY)
            '''
            if self.detect_april_tags(frame_temp) == INTERSECTION_TAG:
                GPIO.output(self.intersection_pin, True)
            else:
                GPIO.output(self.intersection_pin, False)
            '''

            if self.detect_stop_sign(frame_temp, gray_temp) is not ():
                print ("Detected stop sign")
                GPIO.output(self.stop_sign_pin, True)
            else:
                GPIO.output(self.stop_sign_pin, False)
            self.rawCapture.truncate(0)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # When everything is done, release the capture
        cv2.destroyAllWindows()

    def detect_traffic_lights(self, frame, gray):
        # detect circles in the image
        circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 100)


    def detect_april_tags(self, frame): # trying sending in gray instead of frame
        result = self.detector.detect(frame)
        if result:
            return result[0].tag_family
        else:
            return 0

    def detect_stop_sign(self, frame, gray, example=True):
        # Detect any stop signs in the image using the classifier at various scales.
        stop_signs = self.classifier.detectMultiScale(gray, 1.02, 10)

        if example:
            # Draw a rectangle around each detected sign and display it. 
            for (x,y,w,h) in stop_signs:
                cv2.rectangle(gray,(x,y),(x+w,y+h),(255,0,0),2)
             
            cv2.imshow("frame",gray)
            #self.rawCapture.truncate(0)

        # True if any signs were detected. 
        return stop_signs

detection = DetectSigns()
detection.start()
