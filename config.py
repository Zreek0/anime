from os import environ
from dotenv import load_dotenv, find_dotenv, dotenv_values

ENV = environ.get("ENV")
if not ENV:
	load_dotenv(find_dotenv())
else:
	pass
Config = environ

