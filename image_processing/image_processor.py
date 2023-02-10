#!/usr/bin/env python3

from PIL import Image
import glob

images = glob.glob("./images/*")

extension = ".jpeg"

for image in images:
    file_name = image.split("/")[-1]
    im = Image.open(image)
    im.rotate(270).resize((128, 128)).convert("RGB").save(
        f"./icons/{file_name}{extension}"
    )
