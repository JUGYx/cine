#!/usr/bin/env python3

import subprocess
import api
from utils import fmtc, printerr

def fmtShows(data):
    Number=1
    print(fmtc("none", "Shows:"))
    print(fmtc("red", "\t[00]: ")+fmtc("yellow", "Cancel")+fmtc("none", ".")) 
    for show in data:
        en_title=show['en_title']
        year=show['year']
        try:
            first_category=show['categories'][0]['en_title']
        except KeyError:
            first_category="No category"
        print(fmtc('red',f"\t[{Number:0>2}]: ")+fmtc('yellow', en_title)+fmtc('red', f" | {year}")+fmtc('red', f" | {first_category}."))
        Number+=1
    print()

def info():
    print(fmtc("yellow", "[*] Use one of the following formats to specify season and episode:"))
    print(fmtc("yellow", "\t- ")+fmtc("red", "S[Number]E[Number]")+fmtc("yellow",". Where S is season and E is episode, ")+fmtc("red", "i.e: s1E2")+fmtc("yellow", "."))
    print(fmtc("yellow", "\t- ")+fmtc("red", "Number(, or : or ;)Number")+fmtc("yellow",". Write a comma, colon or a semicolon between season and episode, ")+fmtc("red","i.e: 1,2")+fmtc("yellow","."))
    print()

def play(translation, video):
    try:
        if translation != "":
            out = subprocess.check_output(["mpv",f"--sub-file={translation}",video])
        else:
            out = subprocess.check_output(["mpv",video])
    except FileNotFoundError:
        printerr("mpv not found. install it or add it to the environment path.")
        exit(127)

def episodePage(episode):
    print()
    episodeInfo=api.getEpData(episode)
    while True:
        Number=1
        print(fmtc("none", "Resolutions:"))
        print(fmtc("red", "\t[0]:")+fmtc("yellow", "Cancel")+fmtc("none", "."))
        for resolution in episodeInfo['v']:
            print(fmtc("red", f"\t[{Number}]: ")+fmtc("yellow", resolution['resolution'])+fmtc("none", "."))
            Number+=1
        print()
        Resolution=input(fmtc("none", "Select resolution (Enter=Best):> ")).strip()
        if Resolution == "":
            Resolution=-1
        else:
            try:
                Resolution=int(Resolution)
                if Resolution == 0:
                    return None                    
                Resolution-=1
            except ValueError:
                printerr("Must be a number.")
                continue
        if Resolution >= len(episodeInfo['v']):
                printerr("Select one of the above resolutions.")
                continue
        if episodeInfo['t'] == "":
            print()
            translation=input(fmtc("yellow", "Subtitles not included, subtitle file (optional):> ")).strip()
        else:
            translation=episodeInfo['t']
        play(translation, episodeInfo['v'][Resolution]['videoUrl'])
        return None

def parseSelection(Selection):
    Selection=Selection.lower()
    if "," in Selection or ";" in Selection or ":" in Selection:
        for i in ",:;":
            SelectionList=Selection.split(i)
            if len(SelectionList) == 2:
                if SelectionList[0].isdigit() and SelectionList[1].isdigit():
                    return SelectionList
    if "s" in Selection and "e" in Selection:
        SelectionList=Selection.split("s")
        if len(SelectionList) == 2:
            SelectionList=SelectionList[-1].split("e")
            if len(SelectionList) == 2:
                if SelectionList[0].isdigit() and SelectionList[1].isdigit():
                    return SelectionList 
    printerr("Invalid input specification.")
    info()
    return None
    
def showPage(Show):
    Seasons=api.season(Show)
    print()
    print(fmtc("red", "Title: ")+fmtc("yellow", Show['en_title']))
    print(fmtc("red", "Description: ")+fmtc("yellow", Seasons['1']['1']['en_content']))
    print(fmtc("red", "Date: ")+fmtc("yellow", Show['mDate']))
    print(fmtc("red", "Seasons: ")+fmtc("yellow", len(Seasons)))
    print(fmtc("red", "Categories: "), end="")
    for cat in Show['categories']:
        print(fmtc("yellow", cat['en_title']), end=" ")
    print("\n")
    info()
    while True:
        Selection=input(fmtc("none", "Episode (0=Cancel):> ")).strip()
        if Selection == "0":
            print()
            break
        if Selection == "":
            printerr("No input provided.")
            continue
        Selection = parseSelection(Selection)
        if Selection:
            try:
                episode=Seasons[Selection[0]][Selection[1]]
            except KeyError:
                printerr("Season or episode not found.")
                continue
            episodePage(episode)
            
          
def searchPage():
    PageNumber=0
    Page=False
    Query=""
    Error=False
    while True:
        if not Page and not Error:
            Query=input(fmtc("none", "Search Show")+fmtc("red"," :> ")).strip()
            if Query == "":
                printerr("Search query mustn't be empty.")
                continue
        result=api.look(Query, PageNumber)
        if result == [] or result == None:
            printerr("Nothing found.")
            Page=False
            PageNumber=0
            continue
        fmtShows(result)
        ShowInput=input(fmtc("none", "Select show ")+fmtc("red","(Enter=Next):> ")).strip()
        if ShowInput == "":
            PageNumber+=1
            Page=True
            continue
        try:
            ShowNumber=int(ShowInput)
            if ShowNumber == 0:
                print()
                PageNumber=0
                Page=False
                Error=False
                continue
            Error=False
        except ValueError:
            printerr("Must be a number.")
            Error=True
            continue
        ShowNumber-=1
        if ShowNumber >= len(result):
            printerr("Select one of the above shows.")
            Error=True
            continue
        else:
            Error=False
            Page=False
            PageNumber=0
            showPage(result[ShowNumber])
            
def main():
    print(fmtc("red", "\n****************************"))
    print(fmtc("red", "*         Cinemana         *"))
    print(fmtc("red", "****************************"))
    print(fmtc("red","\n[!] This is not an official client."))
    print(fmtc("yellow", "[*] Ctrl-C to quit.\n[*] Requires mpv to work.\n"))

    searchPage()

    
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        printerr("Terminated...")
        exit(0)
    except EOFError:
        printerr("Terminated...")
        exit(0)        
    
