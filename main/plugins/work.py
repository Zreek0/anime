from AnilistPython import Anilist
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..sql import db
from .helper import *

def eng_name(search_value: str):
	anilist = Anilist()
	anime = anilist.get_anime(search_value)
	eng_name = str(anime["name_english"])
	return eng_name
rss = "https://raw.githubusercontent.com/ArjixGamer/gogoanime-rss/main/gogoanime/gogoanime-rss-sub.xml"

async def u_gogo(rss_link=rss):
	feed = feedparser.parse(rss_link)
	if len(feed.entries) == 0:
		return 
	entry = feed.entries[0]
	if entry.title != db.get(rss_link).link:
		q = get_download_links(entry.link)
		if len(q) == 1:
			print("Checked : " + entry.link)
			return
		db.update(rss_link, entry.title)
		op = await upload_gogoanime(entry, -1001568226560, -1001633233596)
	else:
		print(f"Checked : {entry.link}")
	return

scheduler = AsyncIOScheduler()
scheduler.add_job(u_gogo, "interval", seconds=1, max_instances=5)
scheduler.start()
