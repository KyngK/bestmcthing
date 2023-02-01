# bestmcthing
A small collaborative project, inspired by [this](https://www.youtube.com/watch?v=ALy6e7GbDRQ) video by Tom Scott, in an attempt to find the best Minecraft thing.

## Scraping
The following information was grabbed from the [Minecraft Fandom](https://minecraft.fandom.com) with [pymediawiki](https://github.com/barrust/mediawiki):
- Title
- Summary (first sentence of each page)
- Image (using a custom scraper script)
- URL

All of this information was stored to a JSON file with around 8,000 articles found. We then wrote some cleanup scripts to remove the duplicates, articles on versions, people, etc. until we were left with around 2,000 left. From there, we went through them manually to get the existing list of 971 things.

## Website
The website is currently available at [bestmcthing.ardun.me](https://bestmcthing.ardun.me)

## Backend
To install, clone the repository and install the requirements. `cd backend` and `python main.py` to start it on `localhost:8080`

The API is available at `localhost:8080/ba24d209-064f-41a9-bffc-f5050a574e16`. This UUID was originally put in place to obscure the API, however this didn't end up working for various reasons. When the user initially starts voting, you make an http get request to the base page (`localhost:8080/ba24d209-064f-41a9-bffc-f5050a574e16` if you're developing locally), and that gives you a JSON list. That list contains two dictionaries, each of which contains the item info (image, url, title, summary, id). When the user votes, you send back a get request to `localhost:8080/ba24d209-064f-41a9-bffc-f5050a574e16?0=id&1=id`. The two parameters are `0` and `1`. `0` indicates the ID of the item the user wants to downvote, and `1` indicates the ID of the item the user wants to upvote. The backend then saves this info, and sends back (with that same request) another set of items, and the cycle continues. If the user leaves, and doesn't vote for an item after an hour, the ID won't be valid anymore. Also if you send a request with IDs that haven't been requested, or IDs that were requested then voted with, the API will pretend like nothing happened but count it as an invalid request, to prevent scripts from spam voting (; If the user wants to skip you can send a skip parameter (`localhost:8080/ba24d209-064f-41a9-bffc-f5050a574e16?0=id&1=id&skip`) and the backend will log a skipped vote.

## Frontend
The frontend can be run by navigating to the `reactjs` directory, running `npm install`, and `npm start`. Please note that the `npm start` command contains some SSL certificate files and hosts it on port 443, so you may want to modify this for your own needs.
