from flask import Flask, render_template, Response
from picamera2 import Picamera2
from PIL import Image
from io import BytesIO

app = Flask(__name__)

class Camera(object):
    def __init__(self):
        self.piCam = Picamera2()
        #self.piCam.preview_configuration.main.size=(128,128) # setting the size
        self.piCam.preview_configuration.main.size = (1536, 864)  # setting the size
        self.piCam.preview_configuration.align() # for non-formal size --> normal size automatically
        self.piCam.configure("preview")  # add the configurations
        self.piCam.start()

    def get_frame(self):
        frame = self.piCam.capture_array()
        pil_image = Image.fromarray(frame)
        pil_image = pil_image.convert('RGB')
        #pil_image = pil_image.resize((128, 128))
        img_io = BytesIO()
        pil_image.save(img_io, 'JPEG')
        img_io.seek(0)
        return img_io.read()

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
