import sys

import requests
import json as JSON
from utils import *

Headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0"}

def getRequest(url):
    try:
        with requests.session() as s:
            response=s.get(url, headers=Headers)
            if response.ok:
                return response
    except requests.exceptions.ConnectionError:
        printerr("HTTP request failed, check your network connection.")
        sys.exit(-3)

def look(query, pn):
    apiUrl=f"https://cinemana.shabakaty.com/api/android/AdvancedSearch?level=0&videoTitle={query}&staffTitle={query}&year=1900,2022&type=series&page="+str(pn)+"&="
    response=getRequest(apiUrl)
    if response:
        json=JSON.loads(response.text)
        return json

def season(show):
    apiUrl="https://cinemana.shabakaty.com/api/android/videoSeason/id/"+show['nb']
    response=getRequest(apiUrl)
    if response:
        json=JSON.loads(response.text)
        seasons={}
        for i in json:
            seasons[i['season']]={}
        for i in json:
            seasons[i['season']][i['episodeNummer']] = i
        return seasons

def getEpData(episode):
    response_t=getRequest("https://cinemana.shabakaty.com/api/android/allVideoInfo/id/"+episode['nb'])
    response=getRequest("https://cinemana.shabakaty.com/api/android/transcoddedFiles/id/"+episode['nb'])
    if response and response_t:
        json_t=JSON.loads(response_t.text)
        try:
            translation=json_t['translations'][0]['file']
        except KeyError:
            translation=""
        json=JSON.loads(response.text)
        return {"t":translation, "v":json}
