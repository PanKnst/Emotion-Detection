"""Script that extracts,crops and stores images in black and white in a new folder using OpenCVs pre-trained Haar
Cascade-Classifier.
Script adapted from: van Gent, P. (2016). Emotion Recognition With Python, OpenCV and a Face Dataset.
A tech blog about fun things with Python and embedded electronics. Retrieved from:
http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/
"""

import cv2
import glob

# All directories are the directories in which my files are stored, and would change accordingly.

faceDet = cv2.CascadeClassifier("/Users/yenji/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
emotions = ["neutral", "anger", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotions - Removed Contempt


def detect_faces(emotion):
    print(emotion)
    files = glob.glob("/Users/yenji/Desktop/Emotion-Detection/sorted_set_Haar/%s/*" %emotion) #Get list of all images with emotion
    filenumber = 0
    for f in files:
        frame = cv2.imread(f) #Open image
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #Convert image to grayscale

        #Detect face using OpenCVs pre-trained Cascade Classifier:
        face = faceDet.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10, minSize=(5, 5), flags=cv2.CASCADE_SCALE_IMAGE)

        #If a face is detected then store it:
        if len(face) == 1:
        #Cut and save face
            for (x, y, w, h) in face: #get coordinates and size of rectangle containing face
                print ("face found in file: %s" %f)
                gray = gray[y:y+h, x:x+w] #Cut the frame to size
                out = cv2.resize(gray, (350, 350)) #Resize face so all images have same size
                cv2.imwrite("/Users/yenji/Desktop/Emotion-Detection/datasetHaar/%s/%s.jpg" %(emotion, filenumber), out) #Write image
            filenumber += 1 #Increment image number


for emotion in emotions:
    print("Start")
    detect_faces(emotion) #Call functiona
    print("Done")