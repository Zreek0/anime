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

async def u_h20():
	hentai_20 = h20()
	for link in hentai_20.links:
		if link != db.get("H20").link:
			db.update("H20", link)
			try:
				regex = r"{}.*chapter.*-(\d+)".format("https://hentai20.com/")
				ch = re.match(regex, link).group(1)
				pdfname = await post_ws(link, hentai_20.title, ch)
				await app.send_document(-1001676231026, pdfname)
				os.remove(pdfname)
			except Exception as e:
				await app.send_message(-1001676231026, f"**Error :** `{e}`")
				pass
		else:
			print(f"Checked : {hentai_20.title}")
			break
	return

scheduler = AsyncIOScheduler()
scheduler.add_job(u_h20, "interval", seconds=1, max_instances=5)
scheduler.add_job(u_gogo, "interval", seconds=1, max_instances=5)
scheduler.start()
