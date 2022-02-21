import os
import json

with open(os.path.dirname(__file__) + "/config.json", "r") as file:
    data = json.load(file)
    token = data["token"]
    prefix = data["prefix"]
    auto_ban = data["auto_ban"]
    owner_id = data["owner_id"]


