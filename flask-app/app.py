from flask import Flask, render_template, Response


class Camera(object):
    def __init__(self):
        # Initialize your camera here
        # For example, if you're using picamera:
        from picamera import PiCamera
        self.camera = PiCamera()

    def get_frame(self):
        # Capture a frame from the camera and return it as a JPEG-encoded byte string
        from io import BytesIO
        stream = BytesIO()
        self.camera.capture(stream, 'jpeg')
        return stream.getvalue()


app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
