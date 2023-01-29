from stuff import get_things

things = get_things("./things.json")
exts = ['.png', '.gif', '.jpg', '.svg', '.jpeg']
for thing in things:
    if thing.image == None:
        continue
    index = -1
    foundext = ''
    for ext in exts:
        if ext in thing.image:
            index=thing.image.find(ext)
            foundext = ext
            break
    if index == -1:
        raise BaseException("You forgor this :skull:" + thing.image)
    thing.image = thing.image[0: index + len(foundext)]

print([thing.image for thing in things])