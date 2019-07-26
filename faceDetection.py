"""Face Detection with pre-trained cascade classifier that is available from OpenCV
Steps:
1. Capture video (frame by frame)
2. Convert to black and white(grey)
3. Find faces in frame - using pre-trained classifier
4. Draw rectangle around face
5. Display resulting video (frame by frame) """


#import numpy as np
import cv2

#Initialise video capture with OpenCV
cap = cv2.VideoCapture(0)

#Use pretrained face detection cascade classifier available with OpenCV
cascadePath = "/Users/yenji/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Find faces in frame
    faces = faceCascade.detectMultiScale(gray)

    #Draw recangle around faces
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
