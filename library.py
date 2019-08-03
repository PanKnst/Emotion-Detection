""" In this script, contents of the library will be displayed and from here the path of a file can be returned
Show contents of library and select file to be played or deleted.
"""

import glob
import cv2
import time


videosInLibrary = glob.glob("/Users/yenji/Desktop/Emotion-Detection/Library/*")
print("Files currently in library: ")
for file in videosInLibrary:
    print(file)
fileToPlay = input("Select file to play:")

for file in videosInLibrary:
    currentFile = file[-11:]
    print(currentFile)
    if fileToPlay == currentFile:
        print(file)
        videoToPlay = cv2.VideoCapture(file)
        time.sleep(0.2)
        while videoToPlay.isOpened():
            ret, frame = videoToPlay.read()
            if ret:
                cv2.imshow("Frame", frame)
                if cv2.waitKey(30) & 0xFF == ord('q'): #Wait 30 msecs before changing frame (30fps)
                    break
            else:
                break
videoToPlay.release()
cv2.destroyAllWindows()