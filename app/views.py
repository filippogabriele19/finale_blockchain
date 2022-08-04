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
        else:
            data_to_store = [None, 0, a]
            cache.set(
                a.pk,
                data_to_store,
            )

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
                cached_element = cache.get(pk)
                cached_profile = cached_element[0]
                cached_offer = cached_element[1]
                cached_article = cached_element[2]
                if cached_profile == request.user.profile:
                    message = "You are already the highest bidder"
                    return HttpResponseRedirect("/")
                else:
                    if int(offer_value) > cached_offer:
                        # its a good offer
                        message = "offer executed correctly"
                        data_to_store = [
                            request.user.profile,
                            offer_value,
                            cached_article,
                        ]
                        cache.set(
                            pk,
                            data_to_store,
                        )
                    else:
                        message = "Too low offer"

        return HttpResponseRedirect("/")
    else:
        return HttpResponseRedirect("/")


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
