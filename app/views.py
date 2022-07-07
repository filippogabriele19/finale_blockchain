from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import login
from .models import *
from .createdefaultdata import PopulateDb
from django.core.cache import cache
from django.http import HttpResponseRedirect
import datetime
import pytz
import threading
import time
import json
import hashlib
from web3 import Web3
from django.forms.models import model_to_dict


message = ""
do_it_one_time = True
do_it_one_time2 = True


def home_view(request):
    all_articles = Article.objects.all()

    # create default articles
    if all_articles.count() == 0:
        PopulateDb()
    articles = Article.objects.filter(expiry__gt=datetime.datetime.now())

    for a in articles:
        if cache.get(a.pk):
            last_offer_data = cache.get(a.pk)
            a.final_price = last_offer_data[1]

    global do_it_one_time

    if do_it_one_time:
        # run a task that check continuosly if some auction is ended, so it can assign the Article
        # send an eventually email or message to the user
        # and save the date to the blockchain
        try:
            prof = request.user.profile
            t = threading.Thread(
                target=check_auction_end,
                args=(articles, prof, request),
                daemon=True,
            )
            t.start()
            do_it_one_time = False
        except:
            print("--------------ERROR------------")

    global message
    local_mess = message
    message = ""
    return render(request, "home.html", {"message": local_mess, "articles": articles})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get("first_name")
            user.profile.last_name = form.cleaned_data.get("last_name")
            user.profile.email = form.cleaned_data.get("email")
            user.is_active = True
            user.save()

            login(request, user)
            return render(request, "home.html")

    else:
        form = SignUpForm()
    return render(request, "signup.html", {"form": form})


def profile_view(request):
    articles = Article.objects.filter(user=request.user.profile)
    return render(request, "profile.html", {"articles": articles})


def do_new_offer(request):
    if request.method == "GET":
        offer_value = request.GET["offer"]
        pk = request.GET["pk"]
        if offer_value != " ":
            global message
            print(cache)
            if cache.get(pk):
                last_offer_data = cache.get(pk)
                if last_offer_data[0] == request.user.profile:
                    message = "You are already the highest bidder"
                    return HttpResponseRedirect("/")
                else:
                    if offer_value > last_offer_data[1]:
                        # its a good offer
                        message = "offer executed correctly"
                        data_to_store = [request.user.profile, offer_value]
                        cache.set(
                            pk,
                            data_to_store,
                        )
                    else:
                        message = "Too low offer"
            else:
                # no cache for this item on redis
                # new offer sended correctly
                message = "first offer executed correctly"
                data_to_store = [request.user.profile, offer_value]
                cache.set(
                    pk,
                    data_to_store,
                )
        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


def check_auction_end(articles, profile, request):
    global message
    stop_while = False
    while True:
        utc = pytz.UTC
        global do_it_one_time
        for article in articles:
            f1 = article.expiry
            f2 = datetime.datetime.now().replace(tzinfo=utc)
            if f1 < f2:
                # ended auction
                article.available = False
                if cache.get(article.pk):
                    last_offer_data = cache.get(article.pk)
                    # il prezzo finale è l'ultima offerta
                    article.final_price = last_offer_data[1]
                    article.user = profile
                    # save the winner
                    print(article.name)
                    save_last_offer = Offer(
                        referring_user=profile,
                        referring_article=article,
                        price=last_offer_data[1],
                        datetime=datetime.datetime.now(),
                    )
                    save_last_offer.save()
                    article.save()

                    # winned auction
                    message = "Good job!! U winned an auction. Go to your profile to see details"
                    # do a transaction on blockchain
                    send_data_to_blockchain(profile, article, save_last_offer)
                stop_while = True
        if stop_while:
            break
        time.sleep(6)

    # refresh home
    global do_it_one_time
    do_it_one_time = True

    return home_view(request)


def send_data_to_blockchain(profile, article, save_last_offer):
    # do a single element
    my_data = {
        "profile": model_to_dict(profile),
        "article": model_to_dict(article),
        "offer": model_to_dict(save_last_offer),
    }
    tmpObj = json.dumps(my_data, indent=4, sort_keys=True, default=str)
    # convert to json
    # json_string = json.dumps(data)
    # calculate hash
    hash = hashlib.sha256(tmpObj.encode("utf-8")).hexdigest()

    w3 = Web3(
        Web3.HTTPProvider(
            "https://ropsten.infura.io/v3/4047625becb441bcaa7c4f6adc9e9b63"
        )
    )
    # account = w3.eth.account.create()
    # privateKey = account.privateKey.hex()
    address = "0xD4fF629856f24BEdF718B7f2aF2542135e85282B"
    privateKey = "0x337bc7c6b1c39a9d5943d167634dda8f7e3ddf847c02047a73161864e6c5b31c"
    # send transaction
    nonce = w3.eth.getTransactionCount(address)
    gasPrice = w3.eth.gasPrice
    balance = w3.eth.get_balance(address)
    print("- il balance è ", balance)
    value = w3.toWei(0, "ether")
    signedTx = w3.eth.account.signTransaction(
        dict(
            nonce=nonce,
            gasPrice=gasPrice,
            gas=100000,
            to="0x0000000000000000000000000000000000000000",
            value=value,
            data=(hash).encode("utf-8"),
        ),
        privateKey,
    )
    tx = w3.eth.sendRawTransaction(signedTx.rawTransaction)
    txId = w3.toHex(tx)
    print(txId)
    return txId
