import cv2
import imutils


def play(path):
    cap = cv2.VideoCapture(path)
    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = imutils.resize(frame, width=600)
            cv2.imwrite('Pic.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('pic.jpg', 'rb').read() + b'\r\n')
            if cv2.waitKey(50) & 0xFF == ord('q'):
                break
    cap.release()
    cv2.destroyAllWindows()
