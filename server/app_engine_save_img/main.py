"""
To test locally, run:
uvicorn main:app --reload --port 5000

Deploy on Google App Engine using:
gcloud app deploy
"""

import base64
import datetime
import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from google.cloud import storage
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    image: str


load_dotenv()
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
app = FastAPI()
storage_client = storage.Client()
bucket = storage_client.bucket(GCS_BUCKET_NAME)

# simulate model initialisation and weights downloading
# time.sleep(10)


@app.post("/image")
async def image(item: Item):

    base64_img_bytes = item.image.encode("utf-8")
    decoded_img_data = base64.decodebytes(base64_img_bytes)

    current_time = datetime.datetime.now()
    # output as '240621-15-09-13.xxx'
    time_str = current_time.strftime("%d%m%y-%H-%M-%S.%f")

    # with open("test.jpg", "wb") as f_output:
    #     f_output.write(decoded_img_data)
    blob = bucket.blob(f"result_{time_str}.jpeg")
    blob.upload_from_string(decoded_img_data)

    return item.name
