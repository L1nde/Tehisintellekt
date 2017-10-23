#!/usr/bin/env python
# coding: utf-8

# MTAT.06.008 Tehisintellekt I (2017 sügis)
# Koduülesanne 3. Kabe

# Käsureaga kasutajaliides
# Fail, mida koduse töö esitamisel EI SAADETA

import MänguStrateegia.checkers_ai_eatOnly

# Muutujate algväärtustamine ========================================================================================
# Nuppude asukohad kujul 
# [[Mustade nuppude asukohad listidena [rida, veerg]][Valgete nuppude asukohad listidena [rida, veerg]]]
from MänguStrateegia import checkers_ai_eatOnly as checkers_ai

tokens = []
for i in [0,6]:
    tokenscol = []
    for j in range(2):
        for k in range(4):
            tokenscol.append([i+j, 2*k-j+1])
    tokens.append(tokenscol)

boardWidth = 8 # Laua suurus
boardRow = [i for i in range(boardWidth)]

players = ["Must", "Valge"] # Mängijad
player = 0 # Käiku tegev mängija (alustab 0 ehk must)

# mõlemad AI
bothAI = True
# Tehisintellekti vastu mängimine (True või False)
playAI = False
# Kas AI mängib mustade (0) või valgete (1) nuppudega (alati alustavad mustad)
AIPlayer = 1

# Funktsioonid ======================================================================================================

# Mängulaua joonistamine     
def drawBoard():
    print("-" * 40)
    for i in range(boardWidth):
        for j in range(boardWidth):
            if [i, j] in tokens[0]:
                print("M\t", end = "")
            elif [i, j] in tokens[1]:
                print("V\t", end = "")
            # Ruudud, mille rea- ja veeruindeksi summa on paaritu, on valged, neisse "ei käida" (tähistatud sidekriipsuga)
            elif (i + j) % 2 == 0:
                print("-\t", end = "")
            # Tühjad "mustad" ruudud (Utähistatud punktiga)
            else:
                print(".\t", end = "")
        print()
        print()
    print("-" * 40)

# Tagastab mängija nupu võimalike käikude listi vastavalt etteantud mänguruudule
# kujul [[<käiguvariant1 reaaadress>, <käiguvariant1 veeruaadress>], [<käiguvariant2 reaaadress>, <käiguvariant2 veeruaadress>]...]
# Kui võimalikud käigud puuduvad, tagastab tühja listi
def getPossMoves(row, col, player):
    possMoves = []
    # Mustad liiguvad ainult allapoole (reaindeks saab ainult suureneda), valged vastupidi
    direction = 1
    opponent = 1
    if player == 1:
        direction = -1
        opponent = 0
    # Naaberruut
    if row+1*direction in boardRow and col+1 in boardRow and [row+1*direction, col+1] not in tokens[0] and [row+1*direction, col+1] not in tokens[1]:
        possMoves.append([row+1*direction, col+1])
    if row+1*direction in boardRow and col-1 in boardRow and [row+1*direction, col-1] not in tokens[0] and [row+1*direction, col-1] not in tokens[1]:
        possMoves.append([row+1*direction, col-1])
    # Vastase nupu võtmine ja seega kahe ruudu võrra liikumine
    if row+2*direction in boardRow and col+2 in boardRow and [row+2*direction, col+2] not in tokens[0] and [row+2*direction, col+2] not in tokens[1] and [row+1*direction, col+1] in tokens[opponent]:
        possMoves.append([row+2*direction, col+2])
    if row+2*direction in boardRow and col-2 in boardRow and [row+2*direction, col-2] not in tokens[0] and [row+2*direction, col-2] not in tokens[1] and [row+1*direction, col-1] in tokens[opponent]:
        possMoves.append([row+2*direction, col-2])
    return possMoves

# Kontroll, kas mäng on lõppenud ehk kas järgmisel mängijal on võimalik kuhugi käia
def isEnd(player):
    answer = False
    possMoves = []
    for token in tokens[player]:
        possMoves1 = getPossMoves(token[0], token[1], player)
        for pM in possMoves1:
            possMoves.append(pM)
    if len(possMoves) < 1:
        answer = True
    return answer

# Võitja tagastamine: -1 - viik, 0 - must, 1 - valge
# Võidab see, kellel jääb mängulauale rohkem nuppe, võrdse nuppude arvu puhul on viik
def getWinner():
    result = -1
    if len(tokens[0]) != len(tokens[1]):
        result = [len(tokens[0]), len(tokens[1])].index(max([len(tokens[0]), len(tokens[1])]))
    return result

player = 0
drawBoard()
while True:
    print("Käib", players[player])
    # Korratakse seni, kuni kasutaja sisestab oma nupuga ruudu aadressi ja sobiva tühja sihtruudu aadressi
    while True:
        if playAI and player == AIPlayer or bothAI:
            move = checkers_ai.getTurn(tokens, player)
            print(move)
        else:
            move = input("Järgmine käik <algne rida> <algne veerg> <sihtrida> <sihtveerg>: ")
            move = list(map(int, move.split()))
        print(move)
        if [move[0], move[1]] not in tokens[player]:
            print("Ruudus [", move[0], move[1],"] pole sellel mängijal nuppu!")
            continue
        possMoves = getPossMoves(move[0], move[1], player)
        print(possMoves)
        if [move[2], move[3]] not in possMoves:
            print("Ruutu [", move[2], move[3],"] ei saa käia!")
            continue
        break
    # Nupuasukohtade järjendist vana kustutamine ja uue lisamine
    tokens[player].remove([move[0], move[1]])
    tokens[player].append([move[2], move[3]])
    # Vastase nupu löömise korral selle eemaldamine järjendist
    if abs(move[0]-move[2]) == 2:
        opponent = 1
        if player == 1:
            opponent = 0
        tokens[opponent].remove([min(move[0], move[2])+1, min(move[1], move[3])+1])
    drawBoard()
            
    if player == 0:
        player = 1
    else:
        player = 0
    # Kas uuel mängijal on veel käiguvõimalusi
    end = False
    if isEnd(player):
        # Kui järgmisel mängijal enam käiguvõimalusi pole, teatame, kes võitis või jäi mäng viiki
        winner = getWinner()
        if winner < 0:
            print("Mäng lõppes viigiga.")
        else:
            print("Mäng on lõppenud, võitis " + players[winner] + ".")
        break
