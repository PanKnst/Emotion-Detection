import cv2
import os
import imutils


def record(recording):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    frame = imutils.resize(frame, width=600)
    (height, width) = frame.shape[:2]
    path = "/Users/yenji/Desktop/Emotion-Detection"
    fourcc = cv2.VideoWriter_fourcc("C","J","P","G")
    Output = cv2.VideoWriter(os.path.join(path, "Output" + "2" + ".mov"), fourcc, 20, (width, height))

    # Use pretrained face detection cascade classifier available with OpenCV
    faceCascade = cv2.CascadeClassifier("/Users/yenji/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

    # Use fisher_face face detector that has been trained to detect emotions.
    fisher_face = cv2.face.FisherFaceRecognizer_create()
    fisher_face.read('/Users/yenji/Desktop/Emotion-Detection/emotion_detection_model_Haar(fisher).xml')

    emotions = ["neutral", "anger", "disgust", "fear", "happy", "sadness", "surprise"]  # Removed Contempt


    while(recording == True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame = imutils.resize(frame, width=600)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        face = faceCascade.detectMultiScale(gray)

        if len(face) == 1:
            # Draw rectangle around face
            for (x, y, w, h) in face:  # get coordinates and size of rectangle containing face
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                gray = gray[y:y + h, x:x + w]  # Cut rectangle to face size
                gray = cv2.resize(gray, (350, 350))
                label, confidence = fisher_face.predict(gray)  # Get current emotion in face
                cv2.putText(frame, emotions[label], (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.65, (0, 255, 0),
                            1)  # Put emotion found in face on rectangle containing face

        Output.write(frame)
        # Display the resulting frame
        #cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            recording = False
            break

    # When everything done, release the capture
    cap.release()
    Output.release()
    cv2.destroyAllWindows()