""" Script that uses the pre-trained emotion-detection (FisherFace) algorithm to detect emotions in a video stream.
This then displays the resulting image. In the resulting image the face that has been detected has a rectangle around it
with the emotion detected in the face printed on the rectangle.
"""

import cv2
import imutils
import time

#Initialise video capture with OpenCV
cap = cv2.VideoCapture(0)

#Use pretrained face detection cascade classifier available with OpenCV
faceCascade = cv2.CascadeClassifier("/Users/yenji/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

#Use fisher_face face detector that has been trained to detect emotions.
fisher_face = cv2.face.FisherFaceRecognizer_create()
fisher_face.read('/Users/yenji/Desktop/Emotion-Detection/emotion_detection_model_Haar(fisher).xml')

emotions = ["neutral", "anger", "disgust", "fear", "happy", "sadness", "surprise"]#Removed Contempt


def emotionDetection():
    old_emotion = "None"
    emotion_times = [0,0,0,0,0,0,0]
    start = time.time()
    overall_time = 0
    while(True):

        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face = faceCascade.detectMultiScale(gray)

        if len(face) == 1:
            # Draw rectangle around face
            for (x, y, w, h) in face:  # get coordinates and size of rectangle containing face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                gray = gray[y:y + h, x:x + w] #Cut rectangle to face size
                gray = cv2.resize(gray, (350, 350))
                label, confidence = fisher_face.predict(gray) #Get current emotion in face

                current_emotion_index = label
                current_emotion = emotions[label]
                if current_emotion != old_emotion:
                    stop = time.time()
                    duration = stop - start
                    start = time.time()
                    emotion_times[current_emotion_index] += duration
                    old_emotion = current_emotion

                cv2.putText(frame, emotions[label], (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0),
                            1)  # Put emotion found in face on rectangle containing face

        # Display the resulting frame
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    for x in emotion_times:
        overall_time += x
    print("Overall time: " + str(overall_time))
    print(emotion_times)

    cap.release()
    cv2.destroyAllWindows()

emotionDetection()
