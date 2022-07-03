import os
import time
import logging

from os import path, makedirs, remove
from pyrogram import Client, idle
from config import Config

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if __name__ == "__main__":
	if path.isdir("./downloads"):
		os.mkdir("./downloads")
	plugins = dict(root="plugins")
	bot = Client("Auto-Anime", bot_token=Config.get("BOT_TOKEN"), api_id=Config.get("API_ID"), api_hash=Config.get("API_HASH"), plugins=plugins)
	bot.run()
	logger.info("Successfully started bot")
