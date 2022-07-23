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
		await fast_download(i, file.name, headers=dict(Referer=r.url))
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

class h20:
 def __init__(self):
  response = cloudscraper.create_scraper().get("https://hentai20.com/")
  response.raise_for_status()
  soup = BeautifulSoup(response.text, "html.parser")
  data = soup.find("div", "item-summary").find("a")
  self.title = data.text
  self.links = []
  self.chapters = []
  new_data = soup.find_all("span", "c-new-tag")
  for n in new_data:
   n = n.find("a", href=re.compile(data["href"]))
   if n:
    self.links.append(n["href"])
    regex = r"{}.*chapter.*-(\d+)".format(data["href"])
    self.chapters.append(re.match(regex, n["href"]).group(1))
    continue
  self.chapters.reverse()
  self.links.reverse()

class u_manga():
	def __init__(self):
		response = cloudscraper.create_scraper().get("https://manganato.com/")
		response.raise_for_status()
		soup = BeautifulSoup(response.text, "html.parser")
		data = soup.find("div", "content-homepage-item-right").find_all("p", "a-h item-chapter")
		self.title = None
		self.links = []
		for elem in data:
			if "mins" in elem.i.text:
				self.links.append(elem.a["href"])
				self.title = elem.a["title"].split("Chapter ")[0].strip()
		self.links.reverse()
