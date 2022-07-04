from AnilistPython import Anilist
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from . import *

def eng_name(search_value: str):
	anilist = Anilist()
	anime = anilist.get_anime(search_value)
	eng_name = str(anime["name_english"])
	return eng_name
	
fix = []
chat = -1001448819386
async def update_gogoanime():
	feed = feedparser.parse("https://raw.githubusercontent.com/ArjixGamer/gogoanime-rss/main/gogoanime/gogoanime-rss-sub.xml")
	entry = feed.entries[0]
	if not entry.link in fix:
		fix.append(entry.link)
		feed.link = entry.link.replace("gogoanime.vc", "gogoanime.lu")
		download_links = get_download_links(entry.link)
		if "1080p" in download_links:
			dllink = download_links.get("1080p")
			name = "[@Ongoing_Seasonal_Anime] " + entry.title + " (1080p).mp4"
			name = os.path.join(os.getcwd(), name)
			file = SmartDL(dllink, name)
			file.start()
			thumb = generate_thumbnail(name, name + ".jpg")
			caption = f"**{entry.title}**\n\n**• Qᴜᴀʟɪᴛʏ :** 1080p\n**• ᴀᴜᴅɪᴏ :** Japanese\n**• ꜱᴜʙᴛɪᴛʟᴇꜱ :** English"
			await app.send_video(chat, name, thumb=thumb, caption=caption)
			os.remove(name)
			os.remove(thumb)
		if "720p" in download_links:
			dllink = download_links.get("720p")
			name = "[@Ongoing_Seasonal_Anime] " + name + " (720p).mp4"
			name = os.path.join(os.getcwd(), name)
			file = SmartDL(dllink, name)
			file.start()
			thumb = generate_thumbnail(name, name + ".jpg")
			caption = f"**{entry.title}**\n\n**• Qᴜᴀʟɪᴛʏ :** 720p\n**• ᴀᴜᴅɪᴏ :** Japanese\n**• ꜱᴜʙᴛɪᴛʟᴇꜱ :** English"
			await app.send_video(chat, name, thumb=thumb, caption=caption)
			os.remove(name)
			os.remove(thumb)
		if "480p" in download_links:
			dllink = download_links.get("480p")
			name = "[@Ongoing_Seasonal_Anime] " + entry.title + " (480p).mp4"
			name = os.path.join(os.getcwd(), name)
			file = SmartDL(dllink, name)
			file.start()
			thumb = generate_thumbnail(name, name + ".jpg")
			caption = f"**{entry.title}**\n\n**• Qᴜᴀʟɪᴛʏ :** 480p\n**• ᴀᴜᴅɪᴏ :** Japanese\n**• ꜱᴜʙᴛɪᴛʟᴇꜱ :** English"
			await app.send_video(chat, name, thumb=thumb, caption=caption)
			os.remove(name)
			os.remove(thumb)
			
scheduler = AsyncIOScheduler()
scheduler.add_job(update_gogoanime, "interval", minutes=1)
scheduler.start()
