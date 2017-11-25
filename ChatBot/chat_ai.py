#!/usr/bin/env python
# coding: utf-8

# Fail, mida võib muuta ja mis tuleb esitada koduse töö lahendusena
# Faili nime peab jätma samaks
# Faili võib muuta suvaliselt, kuid see peab sisaldama funktsiooni getResponse(),
# millele antakse argumendina ette kasutajalt sisendiks saadud tekst (sõnena)
# ja mis tagastab sobiva vastuse (samuti sõnena)
import urllib.request
import json
import re
import pandas as pd

sonastik = {}
sonastik["[Tt]ere.*"] = "Tervist!"
sonastik["[Ee]i"] = "Jah"

frame = {}
frame["asukoht"] = "Tartu"
frame["aeg"] = "täna"
frame["ilm"] = ""

cities = pd.read_csv("cities.txt", delimiter="\n", index_col=None, header=None)
cities.columns = ["linn"]

stopWords = ["", "Mis", "Missugune", "Kuidas", "Kui", "Palju"]

information = {}

dictionary = {"soe": ["soe", "temperatuur", "külm"], "õhurõhk": ["õhurõhk"], "õhuniiskus": ["õhuniiskus"], "vihm": ["vihm"], "pilved": ["pilved"], "koordinaat": ["koordinaat"], "tuul": ["tuul"]}

def getResponse(text):
    response = "?"
    chocies = proccessInput(text)
    location = ""
    strings = text.split()
    for regex in sonastik.keys():
        if re.match(regex, strings[0]):
            return sonastik[regex]
    for loc in separateLocation(strings):
        lemma = lemmatizer(loc)
        if lemma in cities["linn"].values:
            proccessWeather(getDictFromJson('http://api.openweathermap.org/data/2.5/weather?q=' + lemma + '&units=metric&APPID=' + APPID))
            location = lemma
            break
    # weather = getDictFromJson('http://api.openweathermap.org/data/2.5/weather?q=' + text + '&units=metric&APPID=' + APPID)
    # weather = getDictFromJson('http://api.openweathermap.org/data/2.5/forecast?q=tartu&units=metric&APPID=' + APPID)

    return makeSenteces(chocies, "", location)

def proccessInput(text):
    words = text.split()
    choices = []
    for word in words:
        if word == "ilm":
            choices = dictionary.keys()
            break
        lemma = lemmatizer(word)
        for key, value in dictionary.items():
            if lemma in value:
                choices.append(key)
    return choices

def makeSenteces(choices, time, loc):
    result = form(loc, "in") + " on "
    result = result + ", ".join([information[x] for x in choices])
    return result

def form(word, form):
    file = urllib.request.urlopen('http://prog.keeleressursid.ee/ws_etmrf/syntees.php?c=' + form + '&s=' + urllib.parse.quote(word))
    syntees = json.loads(file.read().decode())
    return syntees["text"]

def proccessWeather(input):
    information["soe"] = "sooja " + str(input["main"]["temp"]) + " " + "kraadi"
    information["õhurõhk"] = "õhurõhk " + str(input["main"]["pressure"]) + " hPa"
    information["õhuniiskus"] = "õhuniiskus " + str(input["main"]["humidity"]) + " " + "protsenti"
    information["temp_min"] = str(input["main"]["temp_min"]) + " kraadi"
    information["temp_max"] = str(input["main"]["temp_max"]) + " kraadi"
    information["vihm"] = input["weather"][0]["description"]
    information["pilved"] = "pilvisus on " + str(input["clouds"]["all"]) + " protsenti"
    information["koordinaat"] = "koordinaadid on " + str(input["coord"]["lon"]) + ", " + str(input["coord"]["lat"])
    information["tuul"] = windDir(input["wind"]["deg"]) + " kiirusega " + str(input["wind"]["speed"]) + " m/s"


def windDir(degrees):
    if 337.5 < degrees <= 360 or 0 <= degrees <= 22.5:
        return "põhjatuul"
    elif 22.5 < degrees <= 67.5:
        return "kirdetuul"
    elif 22.5 < degrees <= 67.5:
        return "kirdetuul"
    elif 67.5 < degrees <= 112.5:
        return "idatuul"
    elif 112.5 < degrees <= 157.5:
        return "kagutuul"
    elif 157.5 < degrees <= 202.5:
        return "lõunatuul"
    elif 202.5 < degrees <= 247.5:
        return "edelatuul"
    elif 247.5 < degrees <= 292.5:
        return "läänetuul"
    elif 292.5 < degrees <= 337.5:
        return "loodetuul"
    else:
        return "arusaamatu suund"


def lemmatizer(word):
    file = urllib.request.urlopen('http://prog.keeleressursid.ee/ws_etmrf/lemma.php?s=' + urllib.parse.quote(word))
    analyys = json.loads(file.read().decode())
    return analyys["root"]

def separateLocation(strings):
    locations = []
    loc = ""
    for string in strings:
        if string[0].isupper():
            loc = " ".join([loc, string])
        else:
            if loc.strip() not in stopWords:
                locations.append(loc.strip())
            loc = ""
    if loc.strip() not in stopWords:
        locations.append(loc.strip())
    return locations


def getDictFromJson(url):
    file = urllib.request.urlopen(url)
    data = json.loads(file.read().decode())
    return data


def getCountryByIso(iso):
    country = "teave puudub"
    # Päring: http://prog.keeleressursid.ee/ws_riigid/index.php?iso=<ISO kood>
    # ISO kahetähelised koodid: https://en.wikipedia.org/wiki/ISO_3166-1
    # Vastus: riigi nimi (eesti keeles)
    file = urllib.request.urlopen("http://prog.keeleressursid.ee/ws_riigid/index.php?iso=" + iso)
    country = file.read().decode()
    return country


# Registreerige ennast http://openweathermap.org/ kasutajaks (ei pea kasutama oma kõige olulisemat e-posti aadressi)
# API Key leiate https://home.openweathermap.org/api_keys, kopeerige see sõnena APPID muutuja väärtuseks
APPID = '60e9f41d0dcbbb6519f413b1f54a1ca4'
