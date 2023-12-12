import cv2
from picamera2 import Picamera2

piCam = Picamera2()
piCam.preview_configuration.main.size=(1280,720) # setting the size
piCam.preview_configuration.main.format=("RGB888")   #turning to BRG as cv2 uses
piCam.preview_configuration.align() # for non-formal size --> normal size automatically
piCam.configure("preview")  # add the configurations
piCam.start()
while True:
    frame = piCam.capture_array()   # get the frame and let cv2 do its magic
    cv2.imshow("piCam",frame)
    if cv2.waitKey(1)==ord("q"):
        break
cv2.destroyAllWindows()