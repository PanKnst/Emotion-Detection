from flask import Flask, render_template, Response, redirect, jsonify, request
from emotionDetectionWeb import emotionDetection
from webpage.recordWeb import VideoCamera
from playVideo import play
import os
import glob


app = Flask(__name__)
variable = False
vc = None

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/library')
def library():
    #Retrieve just the name of each file in the library and pass that to the jija2/html block to display it in a button
    index = 0
    displayFiles=[]
    files = glob.glob("/Users/yenji/Desktop/Emotion-Detection/Library/*")
    for file in files:
        currentFile = file[-11:]
        displayFiles.append(currentFile)
    return render_template('library.html', displayFiles=displayFiles)


#Working here
@app.route('/library/<file>')
def libraryFile(file):
    return render_template('libraryVideoViewer.html', file=file)

@app.route('/libraryVideoPlay/<file>')
def libraryVideoPlay(file):
    path = os.path.join("/Users/yenji/Desktop/Emotion-Detection/Library/", file)
    print(path)
    return Response(play(path),
             mimetype='multipart/x-mixed-replace; boundary=frame')

#@app.route('/libraryMethods', methods = ['POST'])
#def libraryMethods():
    #json = request.get_json()
    #status = json['status']
    #print(status)
    #return jsonify(result="test")

@app.route('/emotionDetectionWeb')
def emotionDetectionWeb():
    return render_template('emotionDetection.html')


@app.route('/recorder', methods = ['POST'])
def recorder():
    global vc
    if vc == None:
        video_camera = VideoCamera()
    vc = VideoCamera()
    json = request.get_json()

    status = json['status']

    if status == "true":
        vc.start_record()
        return jsonify(result="started")
    else:
        vc.stop_record()
        return jsonify(result="stopped")


@app.route('/video_viewer')
def video_viewer():
    return Response(emotionDetection(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    return 'test'


if __name__ == '__main__':
    app.run(debug=True)
