from app import app
from models import Base, engine
from views import AdvertisementView, SpamView
from urls import add_urls


if __name__ == '__main__':

    add_urls(app, AdvertisementView, SpamView)
    Base.metadata.create_all(engine)
    app.run()
