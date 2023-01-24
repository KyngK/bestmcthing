import random
from datetime import datetime
from datetime import timedelta

from flask import Flask, Response, request

from stuff import get_things

app = Flask(__name__)


# flask app
@app.route("/")
def index():
    global buffer
    global things

    args = request.args

    if args and (not '0' in args or not '1' in args):
        return Response("Invalid request", status=400)
    elif args:
        # id of thing to downvote/upvote
        downvote_id = args['0']
        upvote_id = args['1']

        # retrieve matching things
        try:
            downvote = [thing for thing in things if thing.id == downvote_id][0]
            upvote = [thing for thing in things if thing.id == upvote_id][0]

            sent_set = {downvote, upvote}
            matched_set = [s for s in buffer if sent_set & s == sent_set][0]

            # check expiration time
            expire_time = list(matched_set - sent_set)[0]
            if datetime.now() > expire_time:
                buffer.remove(matched_set)
                return Response("Request expired", status=400)

            # update scores
            downvote.score -= 1
            upvote.score += 1

            buffer.remove(matched_set)
        except IndexError:
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


if __name__ == "__main__":
    # open file and create a list of things
    buffer = []
    things = get_things('./things.json')

    app.run(host="localhost", port=8080, debug=True)