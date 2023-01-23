import json
import re

with open('./things.json', 'r') as file:
    data = json.load(file)

exclude = [
    "Tutorials/.*",
    ".*level format",
    "Mods/.*",
    "MINECON.*",
    "Java Edition.*",
    ".*\.png",
    "PlayStation.*",
    ".*/DV2",
    "Bedrock Edition.*",
    "Minecraft:.*",
    "Bedrock Dedicated Server.*",
    "Module:.*",
    "Technical blocks/.*",
    "Xbox 360 Edition.*",
    "MinecraftEDU.*",
    ".*\.png-atlas",
    ".*/DV",
    ".*/ED",
    "Noise generator/.*",
    "Structure/.*",
    "Wii U Edition.*",
    "Cat/.*",
    ".*/BS",
    ".*\(old\)",
    "Launcher.*",
    ".*/BE",
    "Xbox One Edition.*",
    "Chunk format/.*",
    "Widget:.*",
    "Element/.*",
    "Player\.dat format.*",
    ".*\(Outdated\)",
    "Minecraft Education.*",
    "Legacy Console Edition.*",
    ".*/Sounds",
    ".*/History",
    ".*Map:",
    "Invalid Data Value.*",
    ".*/Compasses",
    ".*/OpenPlot",
    "Education Edition.*",
    "Pocket Edition.*",
    ".*/Display",
    ".*/Repairing with Anvils",
    "Redstone circuits/.*",
    ".*/Asset history",
    "Entity format/.*",
    "Narrator.*",
    "Minecraft (Dark Horse Comics).*",
    "Message Wall:.*",
    "Mechanics/.*",
    "Character Creator.*",
    "Featured servers.*",
    "Development resources.*",
    "Custom world generation/.*",
    "Custom dimension/.*",
    "Splash/.*",
    "Mobs of Minecraft/.*",
    "Effect colors/.*",
    "Far Lands/.*",
    "Ore/.*",
    "Minecraft Wiki/.*",
    "Crafting/.*",
    ".*/Structure"
]

allow = [
    "Java Edition",
    "Bedrock Edition",
    "Xbox 360 Edition",
    "MINECON",
    "Wii U Edition",
    "Xbox One Edition",
    "Minecraft Education Edition",
    "Legacy Console Edition",
    "Education Edition",
    "Pocket Edition",
    "Narrator",
    "Mechanics",
]


# initial cleanup
newdata = []
for index, item in enumerate(data):
    if item["title"] in allow:
        newdata.append(item)
        continue
    elif any([re.search(x, item["title"]) for x in exclude]):
        continue
    # elif any([re.search(x, item["title"]) for x in modify]):
    #     item["title"] 
    #     newdata.append(item)
    else:
        newdata.append(item)

# duplicates
dupelist = []
for item in newdata:
    for otheritem in newdata:
        if item["title"] == otheritem["title"]:
            dupelist.append(item["title"])

newdata = [item for item in newdata if item not in dupelist]


# write data to file
with open('./newthings.json', 'w') as file:
    json.dump(newdata, file, indent=4)


# statistics
stats = "Finished! "
stats += f"Found {len(dupelist)} duplicates, "
stats += f"and final JSON data has length of {len(newdata)}"
print(stats)