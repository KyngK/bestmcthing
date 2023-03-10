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
@app.route("/ba24d209-064f-41a9-bffc-f5050a574e16")
def index():
    global buffer
    global things

    args = request.args

    if args and (not '0' in args or not '1' in args):
        votes.append(
            Vote(
                valid=False,
                vote_time=datetime.now(),
                winner=None,
                loser=None,
                skip=False
            )
        )
    elif args:
        # id of thing to downvote/upvote
        downvote_id = args['0']
        upvote_id = args['1']

        # retrieve matching things
        try:
            downvote = None
            upvote = None

            # raises StopIteration if there is no matching
            downvote = next(thing for thing in things if thing.id == downvote_id)
            upvote = next(thing for thing in things if thing.id == upvote_id)

            sent_set = {downvote, upvote}
            matched_set = next(s for s in buffer if sent_set & s == sent_set)

            # check expiration time
            expire_time = list(matched_set - sent_set)[0]
            if datetime.now() > expire_time:
                buffer.remove(matched_set)
            elif not 'skip' in args:
                # update scores
                downvote.score -= 1
                upvote.score += 1

                buffer.remove(matched_set)

                votes.append(
                    Vote(
                        valid=True,
                        vote_time=datetime.now(),
                        winner=upvote,
                        loser=downvote,
                        skip=False
                    )
                )
            else:
                votes.append(
                    Vote(
                        valid=True,
                        vote_time=datetime.now(),
                        winner=upvote,
                        loser=downvote,
                        skip=True
                    )
                )
        except StopIteration:
            votes.append(
                Vote(
                    valid=False,
                    vote_time=datetime.now(),
                    winner=upvote or upvote_id,
                    loser=downvote or downvote_id,
                    skip=bool('skip' in args)
                )
            )

    # return two random things
    # sort list by impressions, ascending
    random.shuffle(things)
    things.sort(key=lambda x: x.votes)

    # get two random things
    try:
        thing1 = things[0]
        thing2 = things[1]

        # increase impressions count
        thing1.impressions += 1
        thing2.impressions += 1

        # add to buffer, and send two things
        expire_time = datetime.now() + timedelta(hours=1)
        buffer.append({thing1, thing2, expire_time})
        return [thing1.json, thing2.json]
    except Exception as e:
        print(e)
        print(datetime.now().strftime("%m/%d/%Y %H:%M:%S"), len(things))
        return []


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
    serve(app, host='127.0.0.1', port=8080, connection_limit=os.getenv('CONNECTION_LIMIT', '5000'), threads=os.getenv('THREADS', '50'))
