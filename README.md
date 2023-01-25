
# mcwiki

A small collaborative project, inspired by Tom Scott's [video](https://www.youtube.com/watch?v=ALy6e7GbDRQ), in an attempt to find the best Minecraft thing.

## scraping

Using the [Minecraft Fandom page](https://minecraft.fandom.com/special:AllPages) containing every article, the following information was grabbed:
- Title
- Summary (first sentence of each page)
- Image (most relevantly associated)
- URL

All of this information was stored to a JSON file with about 120,000 articles found. Scripts were wrote to remove the duplicates, articles on versions and people etc, until we were left with around 2,000 left. From there, they were manually sorted through to get a list of 978 things.

## web
The site is currently a work in progress, but will feature a design similar to Tom Scott's wherein users are given the option to select one of two random elements from the list. They pick the one they consider to be better, and that thing then receives a point.
At the end, whichever thing has the most points is declared the best.

## how it works
To install, just clone the repository and install the requirements. `python main.py` to start it on `localhost:8080`

Requesting is quite simple:
When the user initially starts voting, you make an http get request to the base page (`localhost:8080` if you're developing locally), and that gives you a JSON list. That list contains two dictionaries, each of which contains the item info (image, url, title, summary, id). When the user votes, you send back a get request to `localhost:8080?0=id&1=id`. The two parameters are `0` and `1`. `0` indicates the ID of the item the user wants to downvote, and `1` indicates the ID of the item the user wants to downvote. The backend then saves this info, and sends back (with that same request) another set of items, and the cycle continues. If the user leaves, and doesn't vote for an item after an hour, the ID won't be valid anymore. Also if you send a request with IDs that haven't been requested, or IDs that were requested then voted with, the website will send back 400 (bad request) to prevent spam; you can only vote for things you've already requested. If the user wants to skip you can just send both 0 and 0 (not implemented yet)
