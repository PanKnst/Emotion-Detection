import cv2
import threading
import imutils
import os
import glob
import time
import numpy as np

emotion_times = [0, 0, 0, 0, 0, 0, 0]
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

        cascadePath = "/Users/yenji/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
        self.faceCascade = cv2.CascadeClassifier(cascadePath)
        # Use fisher_face face detector that has been trained to detect emotions.
        self.fisher_face = cv2.face.FisherFaceRecognizer_create()
        self.fisher_face.read('/Users/yenji/Desktop/Emotion-Detection/emotion_detection_model_Haar(fisher).xml')
        self.emotions = ["neutral", "anger", "disgust", "fear", "happy", "sadness", "surprise"]  # Removed Contempt

        self.old_emotion = "None"
        self.emotion_times = emotion_times
        self.start_time = 0
        self.overall_time = 0
        self.stop = 0
        self.duration = 0


    def run(self):
        self.start_time=time.time()
        while self.isRunning:
            ret, frame = self.cap.read()
            #frame = imutils.resize(frame, width=600)
            if frame.all() != None:
                frame = imutils.resize(frame, width=600)

            if ret:
                # Our operations on the frame come here
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                # Find faces in frame
                faces = self.faceCascade.detectMultiScale(gray)

                # Draw recangle around faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    gray = gray[y:y + h, x:x + w]  # Cut rectangle to face size
                    gray = cv2.resize(gray, (350, 350))
                    label, confidence = self.fisher_face.predict(gray)  # Get current emotion in face

                    current_emotion_index = label
                    current_emotion = self.emotions[label]
                    if current_emotion != self.old_emotion:
                        self.stop = time.time()
                        self.duration = self.stop - self.start_time
                        self.start_time = time.time()
                        self.emotion_times[current_emotion_index] += self.duration
                        self.old_emotion = current_emotion
                    #print(self.emotion_times)
                    cv2.putText(frame, self.emotions[label], (x, y),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0),
                                1)  # Put emotion found in face on rectangle containing face
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

    def getTimes(self):
        global emotion_times
        mytimes = emotion_times
        emotion_times = [0,0,0,0,0,0,0]
        return mytimes



