import tempfile
import io
import discord
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
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

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

bot = discord.Bot(prefix='!')

@bot.event
async def on_ready():
    print("Bot is online!")

@bot.command(name="retrieve")
async def retrieve(ctx: discord.ApplicationContext):
    await ctx.defer()
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

    stats = [(
        thing.score,
        thing.votes,
        thing.title,
        # percentage
        str(round((1 - (thing.votes - thing.score)/(2 * thing.votes)) * 100, 2)) + "%"
    ) for thing in things]
    stats.sort(key=lambda x: x[0])

    with tempfile.TemporaryDirectory() as tempd:
        with open(f"{tempd}/buf.txt", 'w') as buf:
            for thing in stats:
                print(thing, file=buf)
        with open(f"{tempd}/buf.txt", 'r') as buf:
            await ctx.send_followup(
                f"Found {len(votes)} votes, {len([vote for vote in votes if vote.valid])} valid",
                file=discord.File(buf)
            )

    #print([(x.e, x.winner, x.loser) for x in votes if hasattr(x, 'e')])
    #print([(vote.vote_time - timedelta(hours=8)).strftime("%m/%d/%Y, %H:%M:%S") for vote in votes])

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)