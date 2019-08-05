import cv2
import threading
import imutils
import os
import glob
import time


class RecordingThread(threading.Thread):
    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True

        self.cap = camera
        ret, frame = self.cap.read()
        frame = imutils.resize(frame, width=600)
        (height, width) = frame.shape[:2]
        path = "/Users/yenji/Desktop/Emotion-Detection/Library/"
        arrayOfFiles = glob.glob("/Users/yenji/Desktop/Emotion-Detection/Library/*")
        number=len(arrayOfFiles)
        fourcc = cv2.VideoWriter_fourcc("C", "J", "P", "G")
        self.out = cv2.VideoWriter(os.path.join(path, "Output" + str(number)+".mov"), fourcc, 20, (width, height))


    def run(self):
        while self.isRunning:
            ret, frame = self.cap.read()
            frame = imutils.resize(frame, width=600) #Or here. Something to do with this anyway.
            if ret:
                #frame = imutils.resize(frame, width=600) -> I think this is where the problem is....
                self.out.write(frame)

        self.out.release()

    def stop(self):
        self.isRunning = False

    def __del__(self):
        self.out.release()


class VideoCamera(object):
    def __init__(self):
        # Open a camera
        self.cap = cv2.VideoCapture(0)

        # Initialize video recording environment
        self.is_record = False
        self.out = None

        # Thread for recording
        self.recordingThread = None

    def __del__(self):
        self.cap.release()

    def get_frame(self):
        ret, frame = self.cap.read()
        frame = imutils.resize(frame, width=600)
        return frame

    def start_record(self):
        self.is_record = True
        self.recordingThread = RecordingThread("Video Recording Thread", self.cap)
        self.recordingThread.start()

    def stop_record(self):
        self.is_record = False
        self.cap.release()

        if self.recordingThread != None:
            self.recordingThread.stop()

