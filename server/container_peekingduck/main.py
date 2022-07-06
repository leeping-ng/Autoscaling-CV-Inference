from pathlib import Path

from fastapi import FastAPI
from peekingduck.pipeline.nodes.model import yolo
from peekingduck.pipeline.nodes.draw import bbox
from pydantic import BaseModel

from src.custom_nodes.input import str_to_img
from src.custom_nodes.output import google_store
from src.custom_nodes.output import local_store


class Item(BaseModel):
    name: str
    image: str


app = FastAPI()

str_to_img_node = str_to_img.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
google_store_node = google_store.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
local_store_node = local_store.Node(pkd_base_dir=Path.cwd() / "src" / "custom_nodes")
yolo_node = yolo.Node(detect_ids=["dog"], weights_parent_dir=Path.cwd() / "weights")
bbox_node = bbox.Node(show_labels=True)


@app.post("/image")
async def image(item: Item):
    str_to_img_input = {"img_str": item.image}
    str_to_img_output = str_to_img_node.run(str_to_img_input)

    img = str_to_img_output["img"]
    yolo_input = {"img": img}
    yolo_output = yolo_node.run(yolo_input)

    bbox_input = {
        "img": img,
        "bboxes": yolo_output["bboxes"],
        "bbox_labels": yolo_output["bbox_labels"],
    }
    _ = bbox_node.run(bbox_input)
    _ = google_store_node.run({"img": img})
    # _ = local_store_node.run({"img": img})

    return item.name
