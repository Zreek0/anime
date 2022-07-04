from main import *

import inspect, re, asyncio, time, sys, os, ffmpeg, logging
from pathlib import Path
from telethon import events
from asyncio import sleep
import requests
import feedparser
import lxml
import lxml.etree

from bs4 import BeautifulSoup as bs
from pySmartDL import SmartDL
from ..fast_telethon import uploader, downloader

from telethon.errors import MessageDeleteForbiddenError, MessageNotModifiedError
from telethon.tl.custom import Message
from telethon.tl.types import MessageService

LOGS = logging.getLogger(__name__)
SUDOS = (5038395271, 5370531116, 5074055497)
async def bash(cmd, run_code=0):
    """
    run any command in subprocess and get output or error."""
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip() or None
    out = stdout.decode().strip()
    if not run_code and err:
        split = cmd.split()[0]
        if f"{split}: not found" in err:
            return out, f"{split.upper()}_NOT_FOUND"
    return out, err

def admin_cmd(pattern=None, command=None, **args):
    args["func"] = lambda e: e.via_bot_id is None
    stack = inspect.stack()
    previous_stack_frame = stack[1]
    file_test = Path(previous_stack_frame.filename)
    file_test = file_test.stem.replace(".py", "")
    allow_sudo = args.get("allow_sudo", False)
    # get the pattern from the decorator
    if pattern is not None:
        if pattern.startswith(r"\#"):
            # special fix for snip.py
            args["pattern"] = re.compile(pattern)
        elif pattern.startswith(r"^"):
            args["pattern"] = re.compile(pattern)
            cmd = pattern.replace("$", "").replace("^", "").replace("\\", "")
        else:
            if len(Config.get("HANDLER")) == 2:
                darkreg = "^" + Config.get("HANDLER")
                reg = Config.get("HANDLER").split(" ")[1]
            elif len(Config.get("HANDLER")) == 1:
                darkreg = "^\\" + Config.get("HANDLER")
                reg = Config.get("HANDLER")
            args["pattern"] = re.compile(darkreg + pattern)
            if command is not None:
                cmd = reg + command
            else:
                cmd = (
                    (reg + pattern).replace("$", "").replace("\\", "").replace("^", "")
                )

    args["outgoing"] = True
    # should this command be available for other users?
    if allow_sudo:
        args["from_users"] = SUDOS
        # Mutually exclusive with outgoing (can only set one of either).
        args["incoming"] = True
        del args["allow_sudo"]

    # error handling condition check
    elif "incoming" in args and not args["incoming"]:
        args["outgoing"] = True

    # add blacklist chats, UB should not respond in these chats
    args["blacklist_chats"] = True
    black_list_chats = list(Config.get("BLACKLIST_CHATS") or "")
    if len(black_list_chats) > 0:
        args["chats"] = black_list_chats

    # add blacklist chats, UB should not respond in these chats
    if "allow_edited_updates" in args and args["allow_edited_updates"]:
        del args["allow_edited_updates"]

    # check if the plugin should listen for outgoing 'messages'

    return events.NewMessage(**args)

async def eor(event, text=None, **args):
    time = args.get("time", None)
    edit_time = args.get("edit_time", None)
    if "edit_time" in args:
        del args["edit_time"]
    if "time" in args:
        del args["time"]
    if "link_preview" not in args:
        args["link_preview"] = False
    args["reply_to"] = event.reply_to_msg_id or event
    if event.out and not isinstance(event, MessageService):
        if edit_time:
            await sleep(edit_time)
        if "file" in args and args["file"] and not event.media:
            await event.delete()
            ok = await event.client.send_message(event.chat_id, text, **args)
        else:
            try:
                try:
                    del args["reply_to"]
                except KeyError:
                    pass
                ok = await event.edit(text, **args)
            except MessageNotModifiedError:
                ok = event
    else:
        ok = await event.client.send_message(event.chat_id, text, **args)

    if time:
        await sleep(time)
        return await ok.delete()
    return ok

async def eod(event, text=None, **kwargs):
    kwargs["time"] = kwargs.get("time", 8)
    return await eor(event, text, **kwargs)

def get_download_links(link):
 session = requests.Session()
 args = {}
 cookies = {}
 cookies["gogoanime"] = "hg9f7phuvd6ccm79k51unu6c62"
 cookies["auth"] = "aplnqLxgJbgtaoyFayGHsnA8ndd8z0BnmuGGwYwDl8BgPk3udnmsQsbW%2B4jXcmkfayLPOTXcZHip799T%2FTkUyg%3D%3D"
 r = session.get(link, cookies=cookies)
 soup = bs(r.text, "lxml")
 download_div = soup.find("div", "cf-download").findAll("a")
 for links in download_div:
  dl_link = links["href"]
  quality = links.text.strip().split("x")[1]
  if quality == "360":
   args["360p"] = dl_link
  elif quality == "480":
   args["480p"] = dl_link
  elif quality == "720":
   args["720p"] = dl_link
  elif quality == "1080":
   args["1080p"] = dl_link
 return args

def generate_thumbnail(in_filename, out_filename):
    probe = ffmpeg.probe(in_filename)
    time = float(probe['streams'][0]['duration']) // 11
    width = probe['streams'][0]['width']
    try:
        (
            ffmpeg
            .input(in_filename, ss=time)
            .filter('scale', width, -1)
            .output(out_filename, vframes=1)
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )
    except ffmpeg.Error as e:
        LOGS.error(e.stderr.decode(), file=sys.stderr)
    return out_filename

