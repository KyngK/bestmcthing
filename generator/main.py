import asyncio
import json
import threading
import time
import sys

import mediawiki
from mediawiki.exceptions import DisambiguationError, PageError
from memory_profiler import profile

minecraft = mediawiki.MediaWiki(url="https://minecraft.fandom.com/api.php")

buffer = []
all_json = []
already_found = []
found = 0

exclude = [
    "File:",
    "User:",
    "Talk:",
    "talk:",
    "Template:",
    "Category:",
    "Dungeons:",
    "Earth:",
    "Help:",
    "Wiki:",
    "Development resources/",
    "Minecraft Story Mode:",
]

async def write():
    global found
    global buffer
    global all_json
    
    while buffer:
        try:
            page = buffer.pop()

            if not page:
                continue

            title = page.title
            url = page.url
            summary = min(
                page.summary[:page.summary.find('. ') + 1],
                page.summary[:page.summary.find('.\n') + 1],
                key=len
            ) or page.summary

            try:
                image = page.images[0]
            except IndexError:
                image = None

            page_json = {
                "title": title,
                "summary": summary,
                "image": image,
                "url": url,
            }

            all_json.append(page_json)

            print(f"{page.pageid} | Buffer: {len(buffer)}")
            print(page.title)
        except Exception as e:
            print(e)
    

def scrape(pageid):
    global buffer
    global found
    global already_found

    try:
        page = minecraft.page(pageid=pageid)
    except (PageError, DisambiguationError, KeyError, AttributeError):
        return

    if any(item in page.title for item in exclude) or page.title in already_found:
        return

    buffer.append(page)
    found += 1
    already_found.append(page.title)
    print(f"Found: {found} | Buffer: {len(buffer)} | {page.title}")


async def main():
    global found
    global buffer

    pageid = 2

    loop = asyncio.get_running_loop()
    
    buffer.append(minecraft.page(pageid=1))

    while True:
        tasks = []

        start_found = found

        for _ in range(1000):
            tasks.append(
                loop.run_in_executor(
                    None, scrape, pageid
                )
            )

            pageid += 1
        
        await asyncio.gather(*tasks)

        end_found = found
        if start_found == end_found:
            break
    
    print("Done scraping!")

    tasks = []
    for _ in range(1000):
        tasks.append(
            asyncio.create_task(
                write()
            )
        )
    
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    start = time.perf_counter()

    print("Starting...") 
    asyncio.run(main())

    with open('./things.json', 'w') as file:
        json.dump(all_json, file, indent=4)
    
    print("Done writing!")

    end = time.perf_counter()
    total_time = round(end - start, 2)

    print(f"Scraped {found} pages in {total_time} seconds.")
