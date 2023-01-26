import json
import uuid
from datetime import datetime


class Thing:
    def __init__(self, title, summary, image, url, json):
        self.title = title
        self.summary = summary
        self.image = image
        self.url = url
        self.json = json

        # add a unique identifier to the json
        self.id = str(uuid.uuid4())
        self.json["id"] = self.id

        self.impressions = 0
        self.votes = 0
        self.score = 0


class Vote:
    def __init__(self,
        address,
        request,
        valid: bool,
        vote_time: datetime,
        winner: Thing,
        loser: Thing,
    ):
        self.address = address
        self.request = request
        self.valid = valid
        self.vote_time = vote_time

        self.winner = winner
        self.loser = loser


def get_things(path):
    things = []

    with open(path, 'r') as file:
        json_things = json.load(file)
        for thing in json_things:
            title = thing["title"]
            summary = thing["summary"]
            image = thing["image"]
            url = thing["url"]

            things.append(Thing(title, summary, image, url, thing))
    
    return things
