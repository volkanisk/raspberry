from flask import Flask, render_template, Response
from picamera2 import Picamera2
from PIL import Image


def get_image(piCam):
    frame = piCam.capture_array()
    pil_image = Image.fromarray(frame)
    pil_image = pil_image.convert('RGB')
    pil_image = pil_image.resize((128,128))
    return pil_image


piCam = Picamera2()
#piCam.preview_configuration.main.size=(1280,720) # setting the size
piCam.preview_configuration.main.size=(128,128) # setting the size
piCam.preview_configuration.align() # for non-formal size --> normal size automatically
piCam.configure("preview")  # add the configurations
piCam.start()

app = Flask(__name__)

def gen():
    while True:
        frame = get_image(piCam)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
