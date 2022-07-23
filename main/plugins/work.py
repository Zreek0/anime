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

async def upload_h20(h20, chat, upload_chat):
	mess = "**New Chapter uploaded on hentai20.com :**\n\n"
	for link, ch in zip(h20.links, h20.chapters):
		mess += f"• [{h20.title} - Chapter {ch}]({link})\n"
	post = await bot.send_message(chat, mess)
	for link, ch in zip(h20.links, h20.chapters):
		try:
			pdfname = await post_ws(link, h20.title, ch)
			await app.send_document(upload_chat, pdfname, caption="**{} - Chapter {}**".format(h20.title, ch))
			os.remove(pdfname)
		except Exception as e:
			await post.edit(f"**Error :** `{e}`")

async def u_h20():
	feed = h20()
	if feed.title != db.get("H20").link:
		db.update("H20", feed.title)
		await upload_h20(feed, -1001568226560, -1001676231026)
	else:
		print(f"Already Uploaded : {feed.title}")
	return
scheduler = AsyncIOScheduler()
scheduler.add_job(u_h20, "interval", seconds=5, max_instances=5)
scheduler.start()
