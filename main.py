import json
import random
import uuid
from datetime import datetime

from flask import Flask, Response, request

app = Flask(__name__)


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


def get_things():
    things = []

    with open('./things.json', 'r') as file:
        json_things = json.load(file)
        for thing in json_things:
            title = thing["title"]
            summary = thing["summary"]
            image = thing["image"]
            url = thing["url"]

            things.append(Thing(title, summary, image, url, thing))
    
    return things


# flask app
@app.route("/")
def index():
    global buffer
    global things

    args = request.args

    if args and (not '0' in args or not '1' in args):
        return Response("", status=400)
    elif args:
        # id of thing to downvote/upvote
        downvote_id = args['0']
        upvote_id = args['1']

        # retrieve matching things
        try:
            downvote = [thing for thing in things if thing.id == downvote_id][0]
            upvote = [thing for thing in things if thing.id == upvote_id][0]
        except IndexError:
            downvote = None
            upvote = None

        if {downvote, upvote} in buffer:
            # update scores
            downvote.score -= 1
            upvote.score += 1

            print(downvote, upvote)
            buffer.remove({downvote, upvote})

    # return two random things
    # sort list by impressions, ascending
    random.shuffle(things)
    things.sort(key=lambda x: x.impressions)

    # get two random things
    thing1 = things[0]
    thing2 = things[1]

    # increase impressions count
    thing1.impressions += 1
    thing2.impressions += 1

    # add to buffer, and send two things
    buffer.append({thing1, thing2})
    return [thing1.json, thing2.json]


if __name__ == "__main__":
    # open file and create a list of things
    buffer = []
    things = get_things()

    app.run(host="localhost", port=8080, debug=True)