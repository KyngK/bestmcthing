# mcwiki
A small collaborative project, inspired by [this](https://www.youtube.com/watch?v=ALy6e7GbDRQ) video by Tom Scott, in an attempt to find the best Minecraft thing.

## Scraping
The following information was grabbed from the [Minecraft Fandom](https://minecraft.fandom.com) with [pymediawiki](https://github.com/barrust/mediawiki):
- Title
- Summary (first sentence of each page)
- Image (using a custom scraper script)
- URL

All of this information was stored to a JSON file with around 8,000 articles found. We then wrote some cleanup scripts to remove the duplicates, articles on versions, people, etc. until we were left with around 2,000 left. From there, we went through them manually to get the existing list of 978 things.

## Website
The site is currently a work in progress, but will feature a design similar to Tom Scott's wherein users are given the option to select one of two random elements from the list. They pick the one they consider to be better, and that thing then receives a point.

At the end, whichever thing has the most points is declared the best.

## Backend (temporary notes)
To install, clone the repository and install the requirements. `python main.py` to start it on `localhost:8080`

Requesting is simple:
The API is available at `localhost:8080/api`. When the user initially starts voting, you make an http get request to the base page (`localhost:8080/api` if you're developing locally), and that gives you a JSON list. That list contains two dictionaries, each of which contains the item info (image, url, title, summary, id). When the user votes, you send back a get request to `localhost:8080/api?0=id&1=id`. The two parameters are `0` and `1`. `0` indicates the ID of the item the user wants to downvote, and `1` indicates the ID of the item the user wants to upvote. The backend then saves this info, and sends back (with that same request) another set of items, and the cycle continues. If the user leaves, and doesn't vote for an item after an hour, the ID won't be valid anymore. Also if you send a request with IDs that haven't been requested, or IDs that were requested then voted with, the website will send back 400 (bad request) to prevent spam; you can only vote for things you've already requested. If the user wants to skip you can send a skip parameter (`localhost:8080/api?0=id&1=id&skip`) and the backend will ignore it.