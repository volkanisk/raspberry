import requests
import base64
from io import BytesIO
import json

class ConnectionControl():
    def __init__(self, user_id):
        self.url = "18.206.230.56:5002"
        self.plant_exists = True
        self.user_id = user_id
        return

    def check_plants(self, len_img):
        url = f'http://18.206.230.56:5002/user/{self.user_id}/plants'
        headers = {'Content-Type': 'application/json'}
        payload = {
        }
        response = requests.get(url, json=payload, headers=headers)
        response_json = response.text
        response_list = json.loads(response_json)
        element_count = len(response_list)
        if element_count != len_img or element_count == 0:
            self.plant_exists = False

    def send_image_controller(self,image_array):
        self.check_plants(len(image_array))
        for index, image in enumerate(image_array):
            if self.plant_exists:
                self.send_image(index, image)
            else:
                self.create_plant()
                self.send_image(index, image)

    def send_image(self, plantOrder, plantImage):
        url = self.url + "/plantImage"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'base64': plantImage,  # Corrected to pass the user_id as an object with a 'userId' property
            'order': plantOrder,
            "userId": self.user_id  # Corrected variable name from 'type' to 'plant_type' to avoid conflict
        }
        response = requests.post(url, json=payload, headers=headers)
        return response

    def create_plant(self):
        url = self.url + "/plant"
        headers = {'Content-Type': 'application/json'}
        payload = {
            'userId': self.user_id,  # Corrected to pass the user_id as an object with a 'userId' property
            'type': "lettuce"  # Corrected variable name from 'type' to 'plant_type' to avoid conflict
        }
        response = requests.post(url, json=payload, headers=headers)
        return response