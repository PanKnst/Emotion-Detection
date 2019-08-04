from flask import Flask, render_template, Response, redirect, jsonify, request
from emotionDetectionWeb import emotionDetection


app = Flask(__name__)
variable = False

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/library')
def library():
    return render_template('library.html')


@app.route('/emotionDetectionWeb')
def emotionDetectionWeb():
    return render_template('emotionDetection.html')


@app.route('/emotionDetectionTest')
def emotionDetectionTest():
    return Response(emotionDetection(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route ('/button')
def button():
    variable = True
    return redirect('/emotionDetectionWeb')

if __name__ == '__main__':
    app.run()
