# Scrapers

Scrapers are used to provide a stream of existing posts.
They define a source of posts, and a way to retrieve them.
All implemented scrapers are described below.

## `FrontpageScraper`

This is the only implemented scraper.
It simply retrieves the bot's frontpage, and returns the posts on it.
You can choose the category of posts to retrieve
as they are defined by Reddit (hot, top, etc.).
