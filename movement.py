from motorControl import MotorControl




esp_ip = '192.168.43.41'
motor_controller = MotorControl(esp_ip=esp_ip)


image_array = []
for i in range(3):
    motor_controller.actuator("run")
    motor_controller.sleep(3.65)
    motor_controller.actuator("stop")
    motor_controller.sleep(5)


motor_controller.actuator("terminate")





