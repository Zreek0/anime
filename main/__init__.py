import os
import time
import sys
import shutil

from telethon import TelegramClient
from pyrogram import Client
from config import Config

bot = TelegramClient("AutoAnime", Config.get("API_ID"), Config.get("API_HASH")).start(bot_token=Config.get("BOT_TOKEN"))
app = Client("Auto-Anime", bot_token=Config.get("BOT_TOKEN"), api_id=Config.get("API_ID"), api_hash=Config.get("API_HASH"))
