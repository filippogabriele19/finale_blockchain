from django.conf import settings
import requests
from app.models import *
from django.core.cache import cache
import pytz


def my_scheduled_job():
    print("hallo----------------- i am here")
    for cached_element in cache.keys("*"):
        cached_profile = cached_element[0]
        cached_offer = cached_element[1]
        cached_article = cached_element[2]

        t1 = cached_article.expiry
        t2 = datetime.datetime.now().replace(tzinfo=pytz.UTC)
        if t1 < t2:
            # ended auction
            cached_article.available = False
            # il prezzo finale è l'ultima offerta
            cached_article.final_price = cached_offer
            cached_article.user = cached_profile

            save_last_offer = Offer(
                referring_user=cached_profile,
                referring_article=cached_article,
                price=cached_offer,
                datetime=datetime.datetime.now(),
            )
            save_last_offer.save()
            cached_article.save()

            # winned auction
            # message = "Good job!! U winned an auction. Go to your profile to see details"
            # do a transaction on blockchain
            # send_data_to_blockchain(profile, article, save_last_offer)
    # pass
