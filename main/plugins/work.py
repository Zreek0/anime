from AnilistPython import Anilist
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..sql import db
from . import *

def eng_name(search_value: str):
	anilist = Anilist()
	anime = anilist.get_anime(search_value)
	eng_name = str(anime["name_english"])
	return eng_name
rss_links = []
rss_links.append("https://raw.githubusercontent.com/ArjixGamer/gogoanime-rss/main/gogoanime/gogoanime-rss-sub.xml")
for i in rss_links:
	if db.get(i) == None:
		db.update(i, "*")

async def update_gogoanime(i:str = rss_links[0]):
	feed = feedparser.parse(i)
	if len(feed.entries) == 0:
		return 
	entry = feed.entries[0]
	if entry.title != db.get(i).link:
		entry.link = entry.link.replace(".vc", ".lu")
		await upload_gogoanime(entry, entry.link, -1001568226560, -1001726115978)
		db.update(i, entry.title)
	else:
		print(f"Checked : {entry.link}")
	return

scheduler = AsyncIOScheduler()
scheduler.add_job(update_gogoanime, "interval", minutes=5)
scheduler.start()
	
	
	
