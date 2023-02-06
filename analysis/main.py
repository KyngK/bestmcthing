import os
import tempfile

import discord
import stuff
from analyze import *

HOME = os.getenv("HOME")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = discord.Bot()

@bot.event
async def on_ready():
    print("Bot is connected to Discord!")

@bot.command(name="retrieve")
async def retrieve(ctx):
    await ctx.defer()

    buf, votes, things = reconstruct()

    with tempfile.TemporaryDirectory() as tempd:
        with open(f"{tempd}/v.txt", 'w') as file:
            file.write(buf)
        
        with open(f"{tempd}/v.txt", 'r') as file:
            things_file = discord.File(file)

    await ctx.send_followup(
        f"Found {len(votes)} votes, {len([vote for vote in votes if vote.valid])} valid",
        file=things_file
    )

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)