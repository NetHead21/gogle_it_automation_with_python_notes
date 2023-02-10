#! /usr/bin/env python3

import requests
from os import listdir
import json


path: str = "./data/feedback/"
files: list = list(listdir(path))
url: str = "http://localhost/feedback"
keys: list = ["title", "name", "date", "feedback"]


def read_file(file) -> list[str]:
    with open(f"{path}{file}", "r") as file_reader:
        lines = file_reader.read().splitlines()
    return lines


for file in listdir(path):
    lines = read_file(file)
    feed_back = dict(zip(keys, lines))
    feed_back_json = json.dumps(feed_back)

    try:
        resp = requests.post(url, data=feed_back_json)
        print("Feedback Added!")
    except Exception as e:
        print(f"POST failed! | Status code: {resp.status_code}")
