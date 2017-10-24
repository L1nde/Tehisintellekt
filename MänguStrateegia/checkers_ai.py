#!/usr/bin/env python
# coding: utf-8

# Fail, mida võib muuta ja mis tuleb esitada koduse töö lahendusena
# Faili nime peaks jätma samaks
# Faili võib muuta suvaliselt, kuid see peab sisaldama funktsiooni getTurn(),
# millele antakse argumendina ette mängijat tähistav number (0 - Must, 1 - Valge) 
# ning mis tagastab selle mängija järgmise käigu järjendi e. listi kujul
# [old1, old2, new1, new2], kus:
# - old1 on käidava nupu algse asukoha reakoordinaat
# - old2 käidava nupu algse asukoha veerukoordinaat 
# - new1 on käidava nupu lõppasukoha reakoordinaat
# - new2 käidava nupu lõppasukoha veerukoordinaat

from copy import deepcopy

tableSize = 8
depth = 2
started = depth

def getTurn(tokens, player):
    ratings = []
    # Arvutab igale võimlikule liigutusele hinnangu
    for token in tokens[player]:
        moves = getPossibleMoves(tokens, token, player)
        if len(moves) != 0:
            for move in moves:
                ratings.append([minimax(updateBoard(tokens, move, player), move, player, 1 if player == 0 else 0), move])
    # Kui mängijal on käigud otsas
    if len(ratings) == 0:
        return [0, 0, 0, 0]
        # raise Exception(("Valgel " if player == 1 else "Mustal ") + "mängijal on käigud otsas.")
    #print(ratings)
    return max(ratings, key=lambda x: x[0])[1]


def minimax(tokens, move, player, currentPlayer, depth=depth):
    ratings = [0]
    if depth == 0:
        return getRating(move, depth)
    for token in tokens[currentPlayer]:
        for possMovement in getPossibleMoves(tokens, token, currentPlayer):
            ratings.append(getRating(possMovement, depth) + minimax(updateBoard(tokens, possMovement, currentPlayer), possMovement, player, 1 if currentPlayer == 0 else 0, depth - 1))
    #print(ratings)
    if currentPlayer == player:
        return max(ratings)
    else:
        return -max(ratings)


# Uuendab laua seisu
def updateBoard(tokens, move, player):
    copy = deepcopy(tokens)
    copy[player].remove(move[:2])
    copy[player].append(move[2:])
    if abs(move[2] - move[0]) > 1:
        copy[1 if player == 0 else 0].remove([move[0] + (move[2] - move[0])/2, move[1] + (move[3] - move[1])/2])
    return copy

# Tagastab võimalikud käigud
def getPossibleMoves(tokens, token, player):
    moves = []

    # Liikumissuund vastavalt mängijale
    direction = -1 if player == 1 else 1

    # Vastane
    opponent = 1 if player == 0 else 0

    # Liikumine paremale võmalik
    if 0 <= (token[0] + direction) < tableSize and 0 <= token[1] + 1 < tableSize:
        # Ainult liikumine
        if [token[0] + direction, token[1] + 1] not in tokens[player] and [token[0] + direction, token[1] + 1] not in tokens[opponent]:
            moves.append([token[0], token[1], token[0] + direction, token[1] + 1])

        # Söömine
        # Laua piirides
        if 0 <= (token[0] + direction * 2) < tableSize and 0 <= token[1] + 2 < tableSize:
            # Vastane on söömisulatuses
            if [token[0] + direction, token[1] + 1] in tokens[opponent]:
                # Vastase taga on tühi koht
                if [token[0] + direction * 2, token[1] + 2] not in tokens[player] and [token[0] + direction * 2, token[1] + 2] not in tokens[opponent]:
                    moves.append([token[0], token[1], token[0] + direction * 2, token[1] + 2])

                    # Liikumine paremale võimalik
    if 0 <= (token[0] + direction) < tableSize and 0 <= token[1] - 1 < tableSize:
        # Ainult liikmune
        if [token[0] + direction, token[1] - 1] not in tokens[player] and [token[0] + direction, token[1] - 1] not in tokens[opponent]:
            moves.append([token[0], token[1], token[0] + direction, token[1] - 1])

        # Söömine
        # Laua piirides
        if 0 <= (token[0] + direction * 2) < tableSize and 0 <= token[1] - 2 < tableSize:
            # Vastane on söömisulatuses
            if [token[0] + direction, token[1] - 1] in tokens[opponent]:
                # Vastase taga on tühi koht
                if [token[0] + direction * 2, token[1] - 2] not in tokens[player] and [token[0] + direction * 2, token[1] - 2] not in tokens[opponent]:
                    moves.append([token[0], token[1], token[0] + direction * 2, token[1] - 2])

    return moves

def getRating(move, depth):
    # Sööb või ei söö
    return (1 if abs(move[2] - move[0]) > 1 else 0) - (2-depth)