#! /usr/bin/env python3

# sourcery skip: avoid-builtin-shadow
import os
import requests
from pprint import pprint


dir: str = "./data/feedback/"
url: str = "http://34.172.40.129/feedback"
format: list = ["title", "name", "date", "feedback"]

for file in os.listdir(dir):
    content = {}

    with open(f"{dir}{file}", "r") as txtfile:
        for counter, line in enumerate(txtfile):
            content[format[counter]] = line.strip()
            # print(f"{counter}: {line.strip()}")
    # try:
    #     resp = requests.post(url, json=content)
    #     print("Feedback added!")
    # except Exception as e:
    #     print(f"POST failed! | Status code: {resp.status_code}")
    pprint(content)
