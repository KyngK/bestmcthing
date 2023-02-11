import json

thingsFile = open("things.json", "r+")
things = json.load(thingsFile)

def getsc(thing):
    title = thing["title"]
    if title[0] == "/":
        return "Command"
    if title in Entities or "entity" in title:
        return "Entity"
    if title in Items or "item" in title :
        return "Item"
    if title in Blocks or "block" in title or "Block" in title:
        return "Block"
    if title in Enchantments:
        return "Enchantment"
    if title in Biomes:
        return "Biome"
    if title in Effects:
        return "Effect"
    if title in Features or "feature" in title:
        return "Feature"
    if title in Structures:
        return "Structure"
    if "Update" in title:
        return "Update"
    if title[-3:] == "Dye":
        return "Dye"
    return "Other"

with open("Blocks.wow", "r") as f:
    Blocks = f.read()
    f.close()
with open("Items.wow", "r") as f:
    Items = f.read()
    f.close()
with open("Entities.wow", "r") as f:
    Entities = f.read()
    f.close()
with open("Enchantments.wow", "r") as f:
    Enchantments = f.read()
    f.close()
with open("Biomes.wow", "r") as f:
    Biomes = f.read()
    f.close()
with open("Effects.wow", "r") as f:
    Effects = f.read()
    f.close()
with open("Features.wow", "r") as f:
    Features = f.read()
    f.close()
with open("Structures.wow", "r") as f:
    Structures = f.read()
    f.close()

for thing in things:
    lastthing = {}
    sc = getsc(thing)
    c = input(f"{thing['title']}, Category? ({sc})")
    if c =="":
        thing["category"] = sc
    else:
        thing["category"] = c
    lastthing = thing
json.dump(things, thingsFile)
