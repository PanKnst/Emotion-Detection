"""Script that extracts,crops and stores images in black and white in a new folder using OpenCVs Deep Neural
Network (Pre-trained for face Detection).
Script is adapted from several sources, with parts taken from each of the following:
1. van Gent, P. (2016). Emotion Recognition With Python, OpenCV and a Face Dataset.
A tech blog about fun things with Python and embedded electronics. Retrieved from:
http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/
2. https://www.pyimagesearch.com/2018/02/26/face-detection-with-opencv-and-deep-learning/
3. https://towardsdatascience.com/extracting-faces-using-opencv-face-detection-neural-network-475c5cd0c260
"""


import cv2
import glob
import numpy as np

# Define paths
prototxt_path = "/Users/yenji/opencv/samples/dnn/face_detector/deploy.prototxt"
caffemodel_path = "/Users/yenji/opencv/samples/dnn/face_detector/res10_300x300_ssd_iter_140000_fp16.caffemodel"

# Read the model
net = cv2.dnn.readNetFromCaffe(prototxt_path, caffemodel_path)
emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotions


def detect_faces(emotion):
    print(emotion)
    files = glob.glob("/Users/yenji/Desktop/Emotion-Detection/sorted_set/%s/*" %emotion) #Get list of all images with emotion
    filenumber = 0
    for f in files:
        frame = cv2.imread(f) #Open image
        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
        net.setInput(blob)
        detections = net.forward()

        # loop over the detections
        for i in range(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

            # filter out weak detections by ensuring the `confidence` is
            # greater than the minimum confidence
            # I have found that a confidence less than 0.95 gives wrong results
            if confidence < 0.95:
                continue

            # compute the (x, y)-coordinates of the bounding box for the
            # object
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # cut, resize, convert to gray and save
            out = frame[startY:endY, startX:+endX]
            out = cv2.resize(out, (350, 350))
            out = cv2.cvtColor(out, cv2.COLOR_BGR2GRAY) #Convert to gray so that it can be used with fisherface
            cv2.imwrite("/Users/yenji/Desktop/Emotion-Detection/datasetDNN/%s/%s.jpg" % (emotion, filenumber), out)  # Write image
        filenumber += 1  # Increment image number


for emotion in emotions:
    print("Start")
    detect_faces(emotion) #Call function
    print("Done")