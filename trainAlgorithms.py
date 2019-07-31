""" Script that trains the Fisherface, EigenFace and LPBH Algorithms. This runs 10 times and stores the trained
Models that have been adapted to recognise emotions instead of faces.
Script adapted from: van Gent, P. (2016). Emotion Recognition With Python, OpenCV and a Face Dataset.
A tech blog about fun things with Python and embedded electronics. Retrieved from:
http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/
"""

import cv2
import glob
import random
import numpy as np
emotions = ["neutral", "anger", "disgust", "fear", "happy", "sadness", "surprise"] #Emotion list - Removed Contempt
fishface = cv2.face_FisherFaceRecognizer.create()
eigenface = cv2.face_EigenFaceRecognizer.create()
lpbh = cv2.face_LBPHFaceRecognizer.create()
data = {}


def get_files(emotion): #Define function to get file list, randomly shuffle it and split 80/20
    files = glob.glob("/Users/yenji/Desktop/Emotion-Detection/datasetHaar/%s/*" %emotion)
    random.shuffle(files)
    training = files[:int(len(files)*0.8)] #get first 80% of file list
    prediction = files[-int(len(files)*0.2):] #get last 20% of file list
    return training, prediction


def make_sets():
    training_data = []
    training_labels = []
    prediction_data = []
    prediction_labels = []
    for emotion in emotions:
        training, prediction = get_files(emotion)
        #Append data to training and prediction list, and generate labels 0-7
        for item in training:
            image = cv2.imread(item) #open image
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grayscale
            training_data.append(gray) #append image array to training data list
            training_labels.append(emotions.index(emotion))
        for item in prediction: #repeat above process for prediction set
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            prediction_data.append(gray)
            prediction_labels.append(emotions.index(emotion))
    return training_data, training_labels, prediction_data, prediction_labels


def run_recognizers():
    training_data, training_labels, prediction_data, prediction_labels = make_sets()
    print("training fisher face classifier")
    print("size of training set is:", len(training_labels), "images")
    fishface.train(training_data, np.asarray(training_labels))
    eigenface.train(training_data, np.asarray(training_labels))
    lpbh.train(training_data, np.asarray(training_labels))
    print("predicting classification set")

    cnt = 0
    correct = 0
    incorrect = 0

    correct_fisher = 0
    incorrect_fisher = 0

    correct_eigen = 0
    incorrect_eigen = 0

    correct_lbph = 0
    incorrect_lbph = 0

    for image in prediction_data:
        pred_fisher, conf_fisher = fishface.predict(image)
        pred_eigen, conf_eigen = eigenface.predict(image)
        pred_lpbh, conf_lbph = lpbh.predict(image)

        if pred_fisher == prediction_labels[cnt]:
            correct_fisher += 1
        else:
            incorrect_fisher += 1
        fisher_score = ((100* correct_fisher)/(correct_fisher + incorrect_fisher))

        if pred_eigen == prediction_labels[cnt]:
            correct_eigen += 1
        else:
            incorrect_eigen += 1
        eigen_score = ((100* correct_eigen)/(correct_eigen + incorrect_eigen))

        if pred_lpbh == prediction_labels[cnt]:
            correct_lbph += 1
        else:
            incorrect_lbph += 1
        lpbh_score = ((100 * correct_lbph) / (correct_lbph + incorrect_lbph))
        cnt += 1

    return fisher_score, eigen_score, lpbh_score


#Now run it
metascore_fisher = []
metascore_eigen = []
metascore_lbph = []

for i in range(0,10):
    correct_fisher, correct_eigen, correct_lbph = run_recognizers()
    #print ("got", correct, "percent correct!")
    print ("Got ", correct_fisher, "Fisher percent correct. Got ", correct_eigen, "Eigen percent correct. Got ", correct_lbph , "percent correct")
    metascore_fisher.append(correct_fisher)
    metascore_eigen.append(correct_eigen)
    metascore_lbph.append(correct_lbph)

print("\n\nend score:(fisher)", np.mean(metascore_fisher), "percent correct!")
print("\n\nend score:(eigen)", np.mean(metascore_eigen), "percent correct!")
print("\n\nend score:(lbph)", np.mean(metascore_lbph), "percent correct!")
fishface.save('/Users/yenji/Desktop/Emotion-Detection/emotion_detection_model_Haar(fisher).xml')
eigenface.save('/Users/yenji/Desktop/Emotion-Detection/emotion_detection_model_Haar(eigen).xml')
lpbh.save('/Users/yenji/Desktop/Emotion-Detection/emotion_detection_model_Haar(lbph).xml')
