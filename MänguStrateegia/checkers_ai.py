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




def getTurn(tokens, player):
    ratings = []
    depth = 2
    # Arvutab igale võimlikule liigutusele hinnangu
    for token in tokens[player]:
        moves = getPossibleMoves(tokens, token, player)
        if len(moves) != 0:
            for move in moves:
                ratings.append([getRating(player, player, move, 2) + minimax(updateBoard(tokens, move, player), player, 1 - player, depth), move])
    # print(ratings)
    return max(ratings, key=lambda x: x[0])[1]


def minimax(tokens, player, currentPlayer, depth):
    ratings = [0]
    if depth == 0:
        return 0
    for token in tokens[currentPlayer]:
        for possMovement in getPossibleMoves(tokens, token, currentPlayer):
            temp = getRating(player, currentPlayer, possMovement, depth) + minimax(updateBoard(tokens, possMovement, currentPlayer), player, 1 - currentPlayer, depth - 1)
            ratings.append(temp)
    if currentPlayer == player:
        # Mängija kõige praeem käik
        return max(ratings)
    else:
        # vastase kõige parem käik ehk käik mis teeb mängijale kõige rohkem kahju
        return min(ratings)


# Uuendab laua seisu
def updateBoard(tokens, move, player):
    copy = deepcopy(tokens)
    copy[player].remove(move[:2])
    copy[player].append(move[2:])
    if abs(move[2] - move[0]) > 1:
        copy[1 - player].remove([move[0] + (move[2] - move[0])/2, move[1] + (move[3] - move[1])/2])
    return copy

# Tagastab võimalikud käigud
def getPossibleMoves(tokens, token, player):
    moves = []
    tableSize = 8

    # Liikumissuund vastavalt mängijale
    direction = -1 if player == 1 else 1

    # Vastane
    opponent = 1 - player

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

def getRating(player, currentPlayer, move, depth):
    # Sööb või ei söö ja millisel sügavusel
    rating = 0
    if abs(move[2] - move[0]) > 1:
        rating = 2 + depth
    # kui vastase käik on
    if player != currentPlayer:
        rating = -rating
    return rating
