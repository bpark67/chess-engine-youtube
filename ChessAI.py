import random
from typing import Counter

pieceScores = {"K": 0, "Q": 9, "B": 3, "N": 3, "p": 1, "R": 5}
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


def findRandomMove(validMoves):
    return validMoves[random.randint(0, len(validMoves) - 1)]


"""
Min Max w/o recursion
"""

# def findBestMoveMinMaxNoRecursion(gs, validMoves):
#     turnMultiplier = 1 if gs.whiteToMove else -1
#     opponentMinMaxScore = CHECKMATE
#     bestPlayerMove = None
#     random.shuffle(validMoves)
#     for playerMove in validMoves:
#         gs.makeMove(playerMove)
#         oppMoves = gs.getValidMoves()
#         if gs.staleMate:
#             opponentMaxScore = STALEMATE
#         elif gs.checkMate:
#             opponentMaxScore = -CHECKMATE
#         else:
#             opponentMaxScore = -CHECKMATE
#             for oppMove in oppMoves:
#                 gs.makeMove(oppMove)
#                 gs.getValidMoves()
#                 if gs.checkMate:
#                     score = CHECKMATE
#                 elif gs.staleMate:
#                     score = STALEMATE
#                 else:
#                     score = -turnMultiplier*scoreMaterial(gs.board)
#                 if score > opponentMaxScore:
#                     opponentMaxScore = score
#                 gs.undoMove()
#         if opponentMaxScore < opponentMinMaxScore:
#             opponentMinMaxScore = opponentMaxScore
#             bestPlayerMove = playerMove
#         gs.undoMove()
#     return bestPlayerMove

"""
Helper Method to make first recursive call
"""


def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    random.shuffle(validMoves)
    counter = 0
    findMoveNegaMaxAlphaBeta(
        gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteToMove else -1
    )
    print(counter)
    return nextMove


def findMoveMinMax(gs, validMoves, depth, whiteToMove):
    global nextMove
    if depth == 0:
        return scoreMaterial(gs.board)

    if whiteToMove:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.makeMove(move)
            nextMoves = gs.getValidMoves()
            score = findMoveMinMax(gs, nextMoves, depth - 1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore


def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMove = gs.getValidMoves()
        score = -findMoveNegaMax(gs, nextMove, depth - 1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove(move)

    return maxScore


def findMoveNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter += 1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    # Move ordering... Evaluate best moves first... We prune out worse branches
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(
            gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier
        )
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
        if maxScore > alpha:  # Pruning
            alpha = maxScore
        if alpha >= beta:
            break
    return maxScore


"""
A Positive score is good for white
A Negative score is good for black
"""


def scoreBoard(gs):
    if gs.checkMate:
        if gs.whiteToMove:
            return -CHECKMATE
        else:
            return CHECKMATE
    elif gs.staleMate:
        return STALEMATE
    score = 0
    for row in gs.board:
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] == "b":
                score -= pieceScores[square[1]]

    return score


"""
Score the board based on material
"""


def scoreMaterial(board):
    score = 0
    for row in board:
        for square in row:
            if square[0] == "w":
                score += pieceScores[square[1]]
            elif square[0] == "b":
                score -= pieceScores[square[1]]

    return score
