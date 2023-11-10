import os
import markdown2
import requests
import base64
from django.shortcuts import render
from decouple import config

# THE LANDING PAGE AND THE DIARY PAGE WILL REQUIRE A SEARCH FUNCTION AND KBAR
# The landing page to be paginated 

def index(request):
    api_url = f"https://api.github.com/repos/mankindjnr/markdown-blog/contents/"
    token = config("TOKEN")
    headers = {'authorization': f'token {token}'}
    resp = requests.get(api_url, headers=headers)
    resp_json = resp.json()

    md_dict = {}
    byte_cards = []

    # extract the cards alone
    for i in range(len(resp_json)):
        if "card" in resp_json[i]["name"]:
            byte_cards.append(resp_json[i]["name"])


    for file in byte_cards:
        card_url = api_url + file
        card_resp = requests.get(card_url)
        content = base64.b64decode(card_resp.json().get("content", "")).decode("utf-8")

        byte = {
            "name": file[:-7]+".md",
            "content": markdown2.markdown(content, extras=["fenced-code-blocks"])
        }

        md_dict[file] = byte

    
    return render(request, "diary/index.html", {
        "cards": md_dict,
        "byte_cards": byte_cards,
    })

def bug(request, card_name):
    api_url = f"https://api.github.com/repos/mankindjnr/markdown-blog/contents/{card_name}"

    resp = requests.get(api_url)
    print(resp.status_code)

    resp_json = resp.json()

    content = resp_json.get("content", "")

    decoded_content = base64.b64decode(content).decode("utf-8")

    return render(request, "diary/full.html",{
        "content": markdown2.markdown(decoded_content, extras=["fenced-code-blocks"]),
        "card_name": card_name
    })
