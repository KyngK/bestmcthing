import tempfile
import os
from datetime import datetime, timedelta
import pickle

import pysftp
import stuff
from dotenv import load_dotenv

load_dotenv()

HOSTNAME = os.getenv("HOSTNAME")
USERNAME = os.getenv("USERNAME")
KEYPATH = os.getenv("KEYPATH")
PORT = int(os.getenv("PORT"))

def merge(tlogs: list, vlogs: list) -> tuple[list, list]:
    # integrity check? TODO
    things = pickle.load(tlogs[0])

    for tlog in tlogs:
        tlog.close()

    votes = []
    for vlog in vlogs:
        data = pickle.load(vlog)
        vlog.close()
        for vote in data:
            votes.append(vote)
    
    return things, votes

with pysftp.Connection(HOSTNAME, USERNAME, KEYPATH, port=PORT) as conn:
    conn.chdir('bestmcthing/backend/logs')

    latest_log = max(
        [
            int(''.join(x for x in fname if x.isdigit()))
            for fname in conn.listdir()
        ]
    )

    with tempfile.TemporaryDirectory() as tempd:
        with open(f"{tempd}/t_buf.pkl", 'wb') as t_buf:
            conn.getfo(f"{latest_log}_t.pkl", t_buf)
        with open(f"{tempd}/v_buf.pkl", 'wb') as v_buf:
            conn.getfo(f"{latest_log}_v.pkl", v_buf)

        t_buf = open(f"{tempd}/t_buf.pkl", 'rb')
        v_buf = open(f"{tempd}/v_buf.pkl", 'rb')

tlogs = [t_buf]
vlogs = [v_buf]

for filename in os.listdir('./analysis/logs/'):
    if 't' in filename:
        tlogs.append(
            open(f'./analysis/logs/{filename}', 'rb')
        )
    elif 'v' in filename:
        vlogs.append(
            open(f'./analysis/logs/{filename}', 'rb')
        )

things, votes = merge(tlogs, vlogs)
print(f"Found {len(votes)} votes, {len([vote for vote in votes if vote.valid])} valid")
for thing in things:
    thing.votes = 0
    thing.score = 0

for vote in votes:
    if vote.valid:
        vote.winner = [thing for thing in things if thing.title == vote.winner.title][0]
        vote.loser = [thing for thing in things if thing.title == vote.loser.title][0]

        vote.winner.score += 1
        vote.loser.score -= 1

        vote.winner.votes += 1
        vote.loser.votes += 1

stats = [(thing.score, thing.votes, thing.title) for thing in things]
stats.sort(key=lambda x: x[0])

for thing in stats:
    print(thing)

#print([(x.e, x.winner, x.loser) for x in votes if hasattr(x, 'e')])
#print([(vote.vote_time - timedelta(hours=8)).strftime("%m/%d/%Y, %H:%M:%S") for vote in votes])
