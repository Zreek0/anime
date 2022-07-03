import glob, logging, asyncio
from pathlib import Path
from .loader import load_plugins
from main import *

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

path = "./main/plugins/*py"
files = glob.glob(path)
for name in files:
	with open(name) as f:
		p = Path(f.name)
		plugin_name = p.stem
		load_plugins(plugin_name.replace(".py", ""))
app.start()
if __name__ == "__main__":
	bot.run_until_disconnected()
	logger.info("✦ Successfully Deployed Bot")
