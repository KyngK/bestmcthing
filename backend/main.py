import os
import pickle
import random
import threading
import time
from datetime import datetime, timedelta

from flask import Flask, Response, request, send_file
from stuff import Vote, get_things
from waitress import serve

app = Flask(__name__)

# flask app
@app.route("/api")
def index():
    global buffer
    global things

    args = request.args

    if args and (not '0' in args or not '1' in args):
        votes.append(
            Vote(
                address=get_remote_address(),
                valid=False,
                vote_time=datetime.now(),
                winner=None,
                loser=None,
            )
        )

        return Response("Invalid request", status=400)
    elif 'skip' in args:
        votes.append(
            Vote(
                address=get_remote_address(),
                valid=True,
                vote_time=datetime.now(),
                winner=None,
                loser=None
            )
        )
    elif args:
        # id of thing to downvote/upvote
        downvote_id = args['0']
        upvote_id = args['1']

        # retrieve matching things
        try:
            # raises StopIteration if there is no matching
            downvote = next(thing for thing in things if thing.id == downvote_id)
            upvote = next(thing for thing in things if thing.id == upvote_id)

            sent_set = {downvote, upvote}
            matched_set = next(s for s in buffer if sent_set & s == sent_set)

            # check expiration time
            expire_time = list(matched_set - sent_set)[0]
            if datetime.now() > expire_time:
                buffer.remove(matched_set)
                return Response("Request expired", status=400)

            # update scores
            downvote.score -= 1
            upvote.score += 1

            buffer.remove(matched_set)

            votes.append(
                Vote(
                    address=get_remote_address(),
                    valid=True,
                    vote_time=datetime.now(),
                    winner=upvote,
                    loser=downvote
                )
            )
        except StopIteration:
            ... # discretely reject but log TODO

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
    expire_time = datetime.now() + timedelta(hours=1)
    buffer.append({thing1, thing2, expire_time})
    return [thing1.json, thing2.json]

@app.route("/assets/pack.jpeg")
def pack_image():
    return send_file("../assets/pack.jpeg", mimetype="image/jpeg")

@app.route("/assets/dirt.png")
def dirt_image():
    return send_file("../assets/dirt.png", mimetype="image/png")


def save():
    global votes
    global things

    # make sure logs dir exists
    if not os.path.isdir("./logs"): 
        os.makedirs("./logs")

    num = 0

    while True:
        num += 1

        filename = f"./logs/{num}_v.pkl"
        with open(filename, 'wb') as file:
            pickle.dump(votes, file)
        
        filename = f"./logs/{num}_t.pkl"
        with open(filename, 'wb') as file:
            pickle.dump(things, file)
        
            time.sleep(3600)

if __name__ == "__main__":
    # open file and create a list of things
    buffer = []
    votes = []
    things = get_things('./things.json')

    save_thread = threading.Thread(target=save)
    save_thread.start()

    #app.run(host="localhost", port=8080, debug=True)
    serve(app, host='0.0.0.0', port=8080)
