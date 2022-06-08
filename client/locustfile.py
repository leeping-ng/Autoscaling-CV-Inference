"""
Start process by running:
locust
Begin load testing by setting parameters here:
http://0.0.0.0:8089
"""

import base64
import os

from dotenv import load_dotenv
from locust import HttpUser, between, task

load_dotenv()

URL = os.getenv("URL")
IMAGE_PATH = "../images/shiba_inu.jpeg"
OBJECT_NAME = "shiba_inu"

with open(IMAGE_PATH, "rb") as image_file:
    image_encoded = base64.b64encode(image_file.read()).decode("utf-8")

data = {"name": OBJECT_NAME, "image": image_encoded}


class WebsiteUser(HttpUser):
    wait_time = between(15, 30)

    @task
    def index(self):
        self.client.post(URL, json=data)
