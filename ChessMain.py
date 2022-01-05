"""
Driver File
- Handle User input
- Display current game state
"""

import pygame as p
from pygame.constants import K_z
import ChessEngine

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
    
    loadImages() # Only do this once
    running = True
    sqSelected = () # No selection initially; Keep track of last selection
    playerClicks = [] # Keep track of player clicks. Two tuples: [(6, 4), (4, 4)]
    
    
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            # Mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
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

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()


"""
Draws the squares on the board
Responsible for all graphics within a current game state
"""

def drawGameState(screen, gs):
    drawBoard(screen) # Draw squares on the board
    # Add in piece highlighting or move suggestions
    drawPieces(screen, gs.board) # Draw pieces on top of the squares

"""
Draw the squares on the board
"""

def drawBoard(screen):
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


if __name__ == "__main__":
    main()