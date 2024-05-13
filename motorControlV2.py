import time
import requests

esp_ip = '192.168.43.183'  # Replace with the actual IP of your ESP8266

class MotorControl():
    def __init__(self, esp_ip='192.168.43.41'):
        self.esp_ip = esp_ip
        self.rpm = 100
        return

    def response_getter(self, response):
        if response.status_code == 200:
            print("Motor command executed successfully")
        else:
            print(f"Failed to {self.action}:", response.text)

    def actuator(self, action, steps=None):
        self.action = action
        if steps is not None:
            response = requests.get(f'http://{self.esp_ip}/stepper/{self.action}?steps={steps}')
        else:
            response = requests.get(f'http://{self.esp_ip}/stepper/{self.action}')
        self.response_getter(response)

    def set_rpm(self, rpm=100):
        self.rpm = rpm
        response = requests.get(f'http://{esp_ip}/stepper/setrpm?rpm={self.rpm}')
        if response.status_code == 200:
            print(f"RPM set to {self.rpm}")
        else:
            print("Failed to set RPM")

    def sleep(self, seconds):
        time.sleep(seconds)

# Example usage:
time_len = 1
motor_controller = MotorControl(esp_ip)
for i in range(1):
    motor_controller.set_rpm(80)
    motor_controller.actuator("run", steps=5000)
    motor_controller.sleep(15)
    motor_controller.actuator("terminate")

