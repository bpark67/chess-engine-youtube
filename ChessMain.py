"""
Driver File
- Handle User input
- Display current game state
"""

import pygame as p
from pygame.constants import K_r, K_z
import ChessEngine, ChessAI

WIDTH = HEIGHT = 512
DIMENSION = 8 # Dimension of a chess board
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 # For animations
IMAGES = {}

"""
Load images. Only load it one time.
Initialize a global dictionary of images
"""

def loadImages():
    pieces = ["wp", "wR", "wN", "wB", "wQ", "wK", "bp", "bN", "bR", "bB", "bQ", "bK"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
# We can access an image by using this dictionary. ex. IMAGES["wp"]

"""
Main driver
Handle user input and update graphics
"""

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    
    validMoves = gs.getValidMoves()
    moveMade = False # Flag variable for when a move is made
    animate = False # Flag variable for when we should aniimate a move
    loadImages() # Only do this once
    running = True
    sqSelected = () # No selection initially; Keep track of last selection
    playerClicks = [] # Keep track of player clicks. Two tuples: [(6, 4), (4, 4)]
    gameOver = False
    playerOne = True # If the human is playing white: True
    playerTwo = False # If the human is playing black: True
    
    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() # x, y coordinate of the mouse
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    if sqSelected == (row, col): # The user clicked the same square twice
                        sqSelected = ()
                        playerClicks = []
                    else:
                        sqSelected = (row, col)
                        playerClicks.append(sqSelected) # Append both clicks
                    if len(playerClicks) == 2:
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])
                                moveMade = True
                                animate = True
                                sqSelected = () # Reset user clicks
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                # Was that the user's second click... Move the piece
            # Key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: # Undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    animate = False
                elif e.key == p.K_r: # Reset the board when 'r' is pressed
                    gs = ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False
                    animate = False


        # AI Move finder logic
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findRandomMove(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True

        if moveMade:
            if animate:
                animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        drawGameState(screen, gs, validMoves, sqSelected)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "Black wins by Checkmate")
            else:
                drawText(screen, "White wins by Checkmate")
        elif gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()

"""
Highlight the square selected and moves for piece selected
"""

def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ("w" if gs.whiteToMove else "b"): # sqSelected is a piece that can be moved
            # Highlight Selected Square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) # Transparency value 0~255... 0 being completely transparent
            s.fill(p.Color(96, 63, 131)) # 153, 0, 17 for red
            screen.blit(s, (c*SQ_SIZE, r*SQ_SIZE))
            # Highlight move squares
            s.fill(p.Color(153, 0, 17))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE*move.endCol, SQ_SIZE*move.endRow))

    if gs.moveLog != []:
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)
        s.fill(p.Color(96, 63, 131))
        screen.blit(s, (SQ_SIZE*gs.moveLog[-1].endCol, SQ_SIZE*gs.moveLog[-1].endRow))



"""
Draws the squares on the board
Responsible for all graphics within a current game state
"""

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) # Draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) # Draw pieces on top of the squares

"""
Draw the squares on the board
"""

def drawBoard(screen):
    global colors
    colors = [p.Color(252, 246, 245), p.Color(123, 154, 204)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c) % 2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Draw the pieces on the board using the current game state
"""

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": # Not empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Animating a move
"""

def animateMove(move, screen, board, clock):
    global colors
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 # Frames to move one square
    frameCount = (abs(dR) + abs(dC))*framesPerSquare
    for frame in range(frameCount+1):
        r, c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        # Erase the pieceMoved from the ending square
        color = colors[(move.endRow +move.endCol) % 2]
        endSquare = p.Rect(move.endCol*SQ_SIZE, move.endRow*SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        # Draw captured piece onto rectangle
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        # Draw the moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(240)

def drawText(screen, text):
    font = p.font.SysFont("Helvetica", 32, True, False)
    textObject = font.render(text, 0, p.Color("black"))
    textLocation = p.Rect(0, 0 , WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    textObject = font.render(text, 0, p.Color("gray"))
    screen.blit(textObject, textLocation.move(2, 2))

if __name__ == "__main__":
    main()