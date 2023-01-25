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
