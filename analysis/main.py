import os

import stuff
from analyze import *

buf, votes, things = reconstruct()

print(f"Found {len(votes)} votes, {len([vote for vote in votes if vote.valid])} valid")

HOME = os.getenv("HOME")

with open(f'{HOME}/Downloads/v.txt', 'w') as file:
    file.write(buf)