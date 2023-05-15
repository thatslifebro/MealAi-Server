import io
from uuid import uuid4

import numpy as np
from PIL import Image
from fastapi import UploadFile
from ultralytics import YOLO

from app.utils.upload_image import *


async def predict_image(file: UploadFile):
    contents = await file.read()
    img = Image.open(io.BytesIO(contents)).convert("RGB")
    img.resize((512, 512))

    model = YOLO("last.pt")
    results = model.predict(conf=0.01, source=img)
    boxes = results[0].boxes

    food_classes = np.array(boxes.cls, dtype="int")
    food_xyxy = np.array(boxes.xyxy, dtype="int")

    crops = []

    def image_up(image: Image, image_key: str):
        with io.BytesIO() as output:
            image.save(output, format="PNG")
            output.seek(0)
            fl = UploadFile(file=output, filename=f"{image_key}.png")
            print(image_key)
            upload_file(fl)

    image_key = str(uuid4())
    image_up(img, image_key)
    origin = {"image_key": image_key}

    for crop_size, food_id in zip(food_xyxy, food_classes):
        crop = img.crop(crop_size)
        image_key = str(uuid4())
        image_up(crop, str(food_id + 1) + "/" + image_key)
        detected = {
            "food_id": int(food_id + 1),
            "image_key": str(food_id + 1) + "/" + image_key,
        }

        crops.append(detected)

    res = {"origin": origin, "crops": crops}
    return res
