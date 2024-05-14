from motorControl import MotorControl

esp_ip = '192.168.43.41'
motor_controller = MotorControl(esp_ip=esp_ip)

motor_controller.actuator("terminate")