from AnilistPython import Anilist
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..sql import db
from .helper import *

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

async def u_gogo(i:str = rss_links[0]):
	feed = feedparser.parse(i)
	if len(feed.entries) == 0:
		return 
	entry = feed.entries[0]
	if entry.title != db.get(i).link:
		entry.link = entry.link.replace(".vc", ".lu")
		op = await upload_gogoanime(entry, entry.link, -1001568226560, -1001726115978)
		if op:
			db.update(i, entry.title)
		else:
			pass
	else:
		print(f"Checked : {entry.link}")
	return
	
	
async def h20_feed():
	hm = h20()
	if not hm:
		logger.info("Update not found on Hentai20.com")
	title = hm.get("title")
	link = hm.get("link")
	ch = hm.get("ch")
	if link != db.get("H20").link:
		mess = await bot.send_message(-1001568226560, f"**New pornhwa chapter uploaded on Hentai20.com -**\n\n• [{title.title()}]({link})")
		try:
			pdfname = await post_ws(link, title.title(), ch)
			xx = await uploader(pdfname, pdfname, time.time(), mess, "Uploading... "+pdfname)
			await bot.send_file(-1001676231026, xx, caption=f"**{title.title()} - Chapter {ch}**")
			os.remove(pdfname)
			await eor(mess, "`Done.`")
			db.update("H20", link)
		except Exception as e:
			await eor(mess, f"**Error :** `{e}`")

scheduler = AsyncIOScheduler()
scheduler.add_job(h20_feed, "interval", minutes=1)
scheduler.start()
			
