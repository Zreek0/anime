from sqlalchemy import Column, String, Numeric, Boolean
from sql import SESSION, BASE

class animebase(BASE):
    __tablename__ = "animebase"
    website = Column(String, primary_key=True)
    link = Column(String)

    def __init__(self, website, link):
        self.website = website
        self.link = link


animebase.__table__.create(checkfirst=True)


def get(website):
    try:
        return SESSION.query(animebase).get(website)
    except:
        return None
    finally:
        SESSION.close()


def update(website, link):
    adder = SESSION.query(animebase).get(website)
    if adder:
        adder.link = link
    else:
        adder = animebase(
            website,
            link
        )
    SESSION.add(adder)
    SESSION.commit()
