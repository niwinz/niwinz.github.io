#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = "Andrey Antukh"
SITENAME = "niwi.nz"
SITEURL = 'http://localhost:8000'

TIMEZONE = "UTC"

PATH = "content"

DEFAULT_PAGINATION = 20
USE_FOLDER_AS_CATEGORY = True

GITHUB = "https://github.com/niwinz"
RELATIVE_URLS = False

THEME = "themes/niwibe"
LOCALE = ["en_US.utf8"]
DEFAULT_LANG = "en_US"

FEED_ALL_RSS = "feeds/all.rss.xml"
CATEGORY_FEED_RSS = "feeds/{slug}.rss.xml"
FILENAME_METADATA = "(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)"

ARTICLE_URL = "{date:%Y}/{date:%m}/{date:%d}/{slug}/"
ARTICLE_SAVE_AS = "{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html"

TEMPLATE_PAGES = {"extra/about.jinja": "about.html"}
STATIC_PATHS = [
    "extra/robots.txt",
    "files",
]

EXTRA_PATH_METADATA = {
    "extra/robots.txt": {"path": "robots.txt"},
}

