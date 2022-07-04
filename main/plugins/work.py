from AnilistPython import Anilist
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..sql.globals import gvarstatus, addgvar
from . import *

def eng_name(search_value: str):
	anilist = Anilist()
	anime = anilist.get_anime(search_value)
	eng_name = str(anime["name_english"])
	return eng_name
	
fix = gvarstatus("GOGO_RSS")
chat = -1001448819386
async def update_gogoanime():
	feed = feedparser.parse("https://raw.githubusercontent.com/ArjixGamer/gogoanime-rss/main/gogoanime/gogoanime-rss-sub.xml")
	entry = feed.entries[0]
	if not entry.title == fix:
		addgvar("GOGO_RSS", entry.title)
		entry.link = entry.link.replace("gogoanime.vc", "gogoanime.lu")
		download_links = get_download_links(entry.link)
		qq = await bot.send_message(-1001568226560, f"**New anime uploaded on gogoanime -**\n[{entry.title}]({entry.link})\n")
		mess = await qq.reply("`Processing ...`")
		if "1080p" in download_links:
			dllink = download_links.get("1080p")
			name = "[@Ongoing_Seasonal_Anime] " + entry.title + " (1080p).mp4"
			name = os.path.join(os.getcwd(), name)
			file = SmartDL(dllink, name, progress_bar=False)
			file.start()
			thumb = generate_thumbnail(name, name + ".jpg")
			caption = f"**{entry.title}**\n\n**• Qᴜᴀʟɪᴛʏ :** 1080p\n**• ᴀᴜᴅɪᴏ :** Japanese\n**• ꜱᴜʙᴛɪᴛʟᴇꜱ :** English"
			xx = await uploader(name, name, time.time(), mess, "Uploading... " + name)
			q1 = await bot.send_file(chat, xx, thumb=thumb, caption=caption, supports_streaming=True)
			os.remove(name)
			os.remove(thumb)
		if "720p" in download_links:
			dllink = download_links.get("720p")
			name = "[@Ongoing_Seasonal_Anime] " + entry.title + " (720p).mp4"
			name = os.path.join(os.getcwd(), name)
			file = SmartDL(dllink, name, progress_bar=False)
			file.start()
			thumb = generate_thumbnail(name, name + ".jpg")
			caption = f"**{entry.title}**\n\n**• Qᴜᴀʟɪᴛʏ :** 720p\n**• ᴀᴜᴅɪᴏ :** Japanese\n**• ꜱᴜʙᴛɪᴛʟᴇꜱ :** English"
			xx = await uploader(name, name, time.time(), mess, "Uploading... " + name)
			q1 = await bot.send_file(chat, xx, thumb=thumb, caption=caption, supports_streaming=True)
			os.remove(name)
			os.remove(thumb)
		if "480p" in download_links:
			dllink = download_links.get("480p")
			name = "[@Ongoing_Seasonal_Anime] " + entry.title + " (480p).mp4"
			name = os.path.join(os.getcwd(), name)
			file = SmartDL(dllink, name, progress_bar=False)
			file.start()
			thumb = generate_thumbnail(name, name + ".jpg")
			caption = f"**{entry.title}**\n\n**• Qᴜᴀʟɪᴛʏ :** 480p\n**• ᴀᴜᴅɪᴏ :** Japanese\n**• ꜱᴜʙᴛɪᴛʟᴇꜱ :** English"
			xx = await uploader(name, name, time.time(), mess, "Uploading... " + name)
			q1 = await bot.send_file(chat, xx, thumb=thumb, caption=caption, supports_streaming=True)
			os.remove(name)
			os.remove(thumb)
			
scheduler = AsyncIOScheduler()
scheduler.add_job(update_gogoanime, "interval", minutes=1)
scheduler.start()
