import base64
import os
import requests

from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("URL")
IMAGE_PATH = "../images/shiba_inu.jpeg"
OBJECT_NAME = "shiba_inu"

with open(IMAGE_PATH, "rb") as image_file:
    # b64encode() encodes into a bytes-like object
    # .decode("utf-8") is a string method (not base64) that converts it to an ASCII string
    # It removes the prefix "b" that would otherwise appear like b"your_string"
    # On the other side, you'll need to encode("utf-8") to change back to bytes object.
    image_encoded = base64.b64encode(image_file.read()).decode("utf-8")

data = {"name": OBJECT_NAME, "image": image_encoded}
requests.post(URL, json=data)
