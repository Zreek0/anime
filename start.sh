cd /app
rm -rf anime
git clone https://github.com/Zreek0/anime anime
cd anime
pip install --quiet -r requirements.txt
python3 -m main 
