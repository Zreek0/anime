import re
import os
import time
from . import *
from bs4 import BeautifulSoup
import shutil
import requests
import threading
import cloudscraper
import img2pdf
import glob
import logging
request = requests.Session()
from reportlab.pdfgen import canvas
from concurrent.futures import ThreadPoolExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from ..sql import db
from PIL import Image

logger = logging.getLogger(__name__)

def create_pdf(path, images: list):
	pdf = canvas.Canvas(path)

	for image in images:

		# noinspection PyBroadException
		try:
			with Image.open(image) as img:
				w, h = img.size

		except BaseException:
			continue

		pdf.setPageSize((w, h))  # Set the page dimensions to the image dimensions

		pdf.drawImage(image, x=0, y=0)  # Insert the image onto the current page

		pdf.showPage()  # Create a new page ready for the next image

	pdf.save()

async def post_ws(link, name, chapter, class_="wp-manga-chapter-img", src="src"):
	chno = str(chapter)
	chno = chno.replace("-", ".")
	pdfname = f"./Chapter {chno} {name}" + " @Adult_Mangas.pdf"
	upr = f"manga{chapter}"
	if not os.path.exists(upr):
		os.mkdir(upr)
	scraper = cloudscraper.create_scraper()
	r = requests.get(link)
	if "hentaidexy" in link or "manhwahub" in link:
		r = scraper.get(link)
		r.raise_for_status()
	elif "toonily" in link:
		r = scraper.get(link)
	else:
		r = requests.get(link)
		r.raise_for_status()
	soup = BeautifulSoup(r.text, "html.parser")
	image_links = soup.find_all("img", class_)
	n = 0
	images = []
	for i in image_links:
		i = i[src].split("\t")[-1]
		n += 1
		file = open(f"./{upr}/{n}.jpg", "wb")
		executor = ThreadPoolExecutor(max_workers=40)
		executor.submit(download, i, file.name, dict(Referer=r.url))
		images.append(file.name)
	with open(pdfname, "wb") as f:
		try:
			f.write(img2pdf.convert(images))
		except Exception as err:
			cmd = os.system(f"convert `ls -tr {upr}/` mydoc.pdf")
			os.rename("mydoc.pdf", pdfname)
			logging.info(err)
		except:
			raise 
	shutil.rmtree(upr)
	return pdfname

def h20(): 
 args = dict()
 r = cloudscraper.create_scraper().get("https://Hentai20.com/")
 r.raise_for_status()
 soup = BeautifulSoup(r.text, "html.parser")
 data = soup.find("div", "c-blog-listing c-page__content manga_content").find("a")
 args["title"] = data["title"]
 link = None
 data_link = soup.find_all("a", href=re.compile(data["href"]))
 data_link.remove(data_link[0])
 data_link.remove(data_link[0])
 args["link"] = data_link[0]["href"]
 ch_input = data_link[0].string.strip()
 ch_regex = r"[^.]hapter (\d+)"
 match = re.match(ch_regex, ch_input)
 args["ch"] = match.group(1)
 return args

