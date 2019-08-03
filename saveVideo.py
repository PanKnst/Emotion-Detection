""" Script that runs face detection and stores the result in the path specified with the name Output.mov
Uses .mov format because that is the one that I have found to work with my macbook and opencv.
"""

#import numpy as np
import cv2
import os

#Initialise video capture with OpenCV
#cap = cv2.VideoCapture(0)

#Read from file. This should be updated so that it reads from the library
cap = cv2.VideoCapture("/Users/yenji/Desktop/Emotion-Detection/Library/Output1.mov")

#To remove, use os.remove(Directory of file to remove)

width = int(cap.get(3))
height = int(cap.get(4))
print(width, height)

path = "/Users/yenji/Desktop/Emotion-Detection"


fourcc = cv2.VideoWriter_fourcc("C","J","P","G")
Output = cv2.VideoWriter(os.path.join(path, "Output2.mov"), fourcc, 5, (width, height))

#Use pretrained face detection cascade classifier available with OpenCV
cascadePath = "/Users/yenji/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()


    #height, width = frame.shape[:2]

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #Find faces in frame
    faces = faceCascade.detectMultiScale(gray)

    #Draw recangle around faces
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    #Output.write(frame)
    # Display the resulting frame
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
Output.release()
cv2.destroyAllWindows()
