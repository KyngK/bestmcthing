import asyncio
import json
import os
import webbrowser

import requests
from bs4 import BeautifulSoup

with open('./things.json', 'r') as file:
    things = json.load(file)

newdata = []

def scrape(thing):
    global newdata

    URL = thing["url"]
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id='content')

    container = results.find_all(class_="infobox-imagearea animated-container")

    start = str(container).find("https://static.wikia.nocookie.net")
    end = str(container)[start:].zfill(len(str(container))).find(">")

    newlink = str(container)[start:end]
    if newlink:
        thing["image"] = newlink
        newdata.append(thing)
        print(newlink, thing['title'])
    else:
        thing["image"] = None
        newdata.append(thing)


async def main():
    loop = asyncio.get_running_loop()
    tasks = []

    for thing in things:
        tasks.append(loop.run_in_executor(None, scrape, thing))

        if len(tasks) > 100:
            await asyncio.gather(*tasks)
            tasks = []
    
    if tasks:
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())

    with open('./image_cleanup.json', 'w') as file:
        json.dump(newdata, file, indent=4)