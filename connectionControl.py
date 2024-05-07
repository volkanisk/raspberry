import requests
import base64
from io import BytesIO
import json

class ConnectionControl():
    def __init__(self, user_id):
       # self.url = "http://18.206.230.56:5002"
       # self.url = " http://localhost:5002"
        self.url = "http://54.237.210.151:5004"
        self.plant_exists = True
        self.user_id = user_id
        return

    def check_plants(self, len_img):
        url = f'{self.url}/user/{self.user_id}/plants'
        headers = {'Content-Type': 'application/json'}
        response = requests.get(url, headers=headers)

        response_list = response.json()
        element_count = len(response_list)
        self.plant_exists = (element_count == len_img) and (element_count != 0)

    def send_image_controller(self,image_array):
        self.check_plants(len(image_array))
        for index, image in enumerate(image_array):
            if not self.plant_exists:
                self.create_plant()
            self.send_image(index, image)

    def send_images_controller(self,image_array):
        self.check_plants(len(image_array))
        for index, image in enumerate(image_array):
            if not self.plant_exists:
                self.create_plant()

        self.send_images(image_array)


    def send_image(self, plantOrder, plantImage):
        url = self.url + "/plantImage"
        img_bytes = BytesIO()
        plantImage.save(img_bytes, format='JPEG')
        img_bytes.seek(0)
        files = {'image': ('image.jpg', img_bytes, 'image/jpeg')}
        data = {
            'order': plantOrder,
            'userId': self.user_id
        }
        response = requests.post(url, files=files, data=data)
        print("Status Code:", response.status_code)  # Debug: Print status code
        print("Response Content:", response.text)
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
        
    def send_images(self,image_array):
        url = f"{self.url}/plantImages"
        files = []
        for index, image in enumerate(image_array):
            img_bytes = BytesIO()
            image.save(img_bytes, format='JPEG')
            img_bytes.seek(0)
            files.append(('images', ('image_{}.jpg'.format(index), img_bytes, 'image/jpeg')))

        data = {'userId': self.user_id}
        response = requests.post(url, files=files, data=data)
        print("Status Code:", response.status_code)
        print("Response Content:", response.text)

'''def encode_file_to_base64(self, image):
        img_bytes = BytesIO()
        image.save(img_bytes, format='PNG')
        # image.save(img_bytes, format='JPEG')
        return base64.b64encode(img_bytes.getvalue()).decode('utf-8') '''
