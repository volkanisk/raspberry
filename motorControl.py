import time
import requests

esp_ip = '192.168.43.41'  # Replace with the actual IP of your ESP8266

class MotorControl():
    def __init__(self, esp_ip = '192.168.43.41'):
        self.esp_ip = esp_ip
        return
    def response_getter(self, response):
        if response.status_code == 200:
            print("Motor turned on successfully")
        else:
            print(f"Failed to {self.action}:", response.text)

    def actuator(self, action):
        self.action = action
        response = requests.get(f'http://{self.esp_ip}/stepper/{self.action}')
        self.response_getter(response)

    def sleep(self, seconds):
        time.sleep(seconds)

# Example usage:
time_len = 0.3
motor_controller = MotorControl(esp_ip)
for i in range(1):
    motor_controller.actuator("run")
    motor_controller.sleep(time_len)
    motor_controller.actuator("stop")
    motor_controller.sleep(time_len)
    motor_controller.actuator("run")
    motor_controller.sleep(2*time_len)
    motor_controller.actuator("stop")
    motor_controller.sleep(2*time_len)
    motor_controller.actuator("terminate")


