"""Script to sort Cohn-Kanade(CK) Dataset. Available at: http://www.consortium.ri.cmu.edu/ckagree/
Citing:
- Kanade, T., Cohn, J. F., & Tian, Y. (2000). Comprehensive database for facial expression analysis. Proceedings of the Fourth IEEE International Conference on Automatic Face and Gesture Recognition (FG'00), Grenoble, France, 46-53.
- Lucey, P., Cohn, J. F., Kanade, T., Saragih, J., Ambadar, Z., & Matthews, I. (2010). The Extended Cohn-Kanade Dataset (CK+): A complete expression dataset for action unit and emotion-specified expression. Proceedings of the Third International Workshop on CVPR for Human Communicative Behavior Analysis (CVPR4HB 2010), San Francisco, USA, 94-101.

Script adapted from: van Gent, P. (2016). Emotion Recognition With Python, OpenCV and a Face Dataset.
A tech blog about fun things with Python and embedded electronics. Retrieved from:
http://www.paulvangent.com/2016/04/01/emotion-recognition-with-python-opencv-and-a-face-dataset/ """

import glob
import natsort
from shutil import copyfile
import os.path

# All directories are the directories in which my files are stored, and would change accordingly.

emotions = ["neutral", "anger", "contempt", "disgust", "fear", "happy", "sadness", "surprise"] #Define emotion order
participants = glob.glob("/Users/yenji/Desktop/Emotion-Detection/source_emotions/*") #Returns a list of all folders with participant numbers
print(participants)
for x in participants:
    part = "%s" %x[-4:] #store current participant number
    print("Current Participant:", part)
    for sessions in glob.glob("%s/*" %x): #Store list of sessions for current participant
        for files in glob.glob("%s/*" %sessions):
            current_session = files[60:-30]
            print(current_session)
            file = open(files, 'r')
            emotion = int(float(file.readline())) #emotions are encoded as a float, readline as float, then convert to integer.
            imagesPath = natsort.natsorted(glob.glob("/Users/yenji/Desktop/Emotion-Detection/source_images/%s/%s/*" % (part, current_session))) #get path for images and sort them
            sourcefile_emotion = imagesPath[-1] #last image in directory contains the emotion
            sourcefile_neutral = imagesPath[0] #first image in directory contains neutral image
            dest_neut = "/Users/yenji/Desktop/Emotion-Detection/sorted_set/neutral/%s" %sourcefile_neutral[63:] #Generate path to put neutral image
            dest_emot = "/Users/yenji/Desktop/Emotion-Detection/sorted_set/%s/%s" %(emotions[emotion], sourcefile_emotion[63:]) #Do same for emotion containing image
            copyfile(sourcefile_neutral, dest_neut) #Copy file
            copyfile(sourcefile_emotion, dest_emot) #Copy file

