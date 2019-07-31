""" Script that streams the emotion detected in the camera feed to a local web-application.
Faces are detected in frames, then for each face detected in a frame, a rectangle is draw around the face. Once this is
done, the emotion displayed in the face is written to the rectangle.
There are a few errors in readings due to lighting and face angles.
"""

from flask import Flask, render_template, Response
import cv2
import imutils

app = Flask(__name__)

@app.route('/')


def index():
    """Video streaming ."""
    return render_template('index.html')


def gen():
    # Initialise video capture with OpenCV
    cap = cv2.VideoCapture(0)

    # Use pretrained face detection cascade classifier available with OpenCV
    faceCascade = cv2.CascadeClassifier("/Users/yenji/opencv/data/haarcascades/haarcascade_frontalface_default.xml")

    # Use fisher_face face detector that has been trained to detect emotions.
    fisher_face = cv2.face.FisherFaceRecognizer_create()
    fisher_face.read('/Users/yenji/Desktop/Emotion-Detection/emotion_detection_model_Haar(fisher).xml')

    emotions = ["neutral", "anger", "disgust", "fear", "happy", "sadness", "surprise"]  # Removed Contempt
    while (True):
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

        # Display the resulting frame
        cv2.imwrite('pic.jpg', frame)
        ##
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True, threaded=True)