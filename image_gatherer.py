from picamera2 import Picamera2
from PIL import Image
from motorControl import MotorControl
from connectionControl import ConnectionControl

img_size = 160
PLANT_COUNT = 4

def get_image(piCam):
    frame = piCam.capture_array()
    pil_image = Image.fromarray(frame)
    pil_image = pil_image.convert('RGB')  
    pil_image = pil_image.resize((img_size,img_size))
    return pil_image

piCam = Picamera2()
#piCam.preview_configuration.main.size=(1280,720) # setting the size
piCam.preview_configuration.main.size=(img_size,img_size) # setting the size
piCam.preview_configuration.align() # for non-formal size --> normal size automatically
piCam.configure("preview")  # add the configurations
piCam.start()

esp_ip = '192.168.43.41'
motor_controller = MotorControl(esp_ip=esp_ip)

connection_id = "664b678ab7b5c9ece4c65be4"
connection_controller = ConnectionControl(user_id=connection_id)

image_array = []
image = get_image(piCam)
connection_controller.send_image(0,image)
image_array.append(image)
for i in range(PLANT_COUNT-1):

    motor_controller.sleep(0.2)
    motor_controller.actuator("run")
    motor_controller.sleep(3.90)
    motor_controller.actuator("stop")
    motor_controller.sleep(0.3)
    image = get_image(piCam)
    connection_controller.send_image(i + 1, image)
    image_array.append(image)
try:
    connection_controller.send_images_controller(image_array)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    motor_controller.actuator("terminate")







