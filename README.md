# mcwiki
(bad name)

## how it works
To install, just clone the repository and install the requirements. `python main.py` to start it on `localhost:8080`

Requesting is quite simple:
When the user initially starts voting, you make an http get request to the base page (`localhost:8080` if you're developing locally), and that gives you a JSON list. That list contains two dictionaries, each of which contains the item info (image, url, title, summary, id). When the user votes, you send back a get request to `localhost:8080?0=id&1=id`. The two parameters are `0` and `1`. `0` indicates the ID of the item the user wants to downvote, and `1` indicates the ID of the item the user wants to downvote. The backend then saves this info, and sends back (with that same request) another set of items, and the cycle continues. If the user leaves, and doesn't vote for an item after an hour, the ID won't be valid anymore. Also if you send a request with IDs that haven't been requested, or IDs that were requested then voted with, the website will send back 400 (bad request) to prevent spam; you can only vote for things you've already requested. If the user wants to skip you can just send both 0 and 0 (not implemented yet)