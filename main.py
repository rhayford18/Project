import pygame
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Checkers")

#Background Constants
Width, Height = 800, 860
Rows, Columns = 8, 8
Size = Width // Columns

Light = (238, 238, 210)
Dark = (118, 150, 86)
Red = (200, 0, 0)
Blue = (0, 0, 0)
White = (0, 0, 225)
Black = (0, 0, 0)

Fps = 60
TurnTime = 60
#Time each player has

#Pieces 
class Piece:
    def __init__(self, row, col, color):
        self.row = row 
        self.col = col
        self.color = color 
    
    def draw(self, screen):
        x = self.col * Size + Size // 2
        y = self.row * Size + Size // 2
        pygame.draw.circle(screen, self.color, (x,y),30)

    def move(self, row, col):
        self.row = row
        self.col = col

#Board 
class Board:
    def __init__(self):
        self.grid[[None for _ in range(Columns) for _ in range(Rows)]]
        self.createpieces()

    def createpieces(self):
        for row in range(Rows):
            for col in range(Columns):
                if (row + col) % 2 == 1:
                    if row < 3:
                        self.grind[row][col] = Piece(row, col, Black)
                    elif row > 4:
                        self.grind[row][col] = Piece(row, col, Red)
    
    def draw(self, screen):
        for row in range(Rows):
            for col in range(Columns):
                color = Dark if (row + col) % 2 else Light
                pygame.draw.rect(
                    screen,
                    color,
                    (col * Size, row * Size, Size, Size)
                )

                piece = self.grid[row][col]
                if piece:
                    piece.draw(screen)
    
    def movepiece(self, piece, row, col):
        self.grid[piece.row][piece.col] = None
        piece.move(row, col)
        self.grid[row][col] = piece 
    
    def remove_piece(self, row, col):
        self.grid[row][col] = None

#Actual Game
class Game:
    def __init__(self, screen):
        self.screen = screen
        self.board = Board
        self.turn = Red 
        self.selected = None 
        self.redtime = TurnTime
        self.blacktime = TurnTime
        self.lasttick = pygame.time.get_ticks()

        self.font = pygame.font.SysFont(None, 32)
        self.gameover = False 
        self.winner = None
    
    #making the timers change
    def updatetimer(self):
        now = pygame.time.get_ticks()
        change = (now - self.lasttick) / 1000
        self.lasttick = now 

        if self.turn == Red:
            self.redtime -= change
            if self.redtime <= 0:
                self.gameover = True
                self.winner = "Black"
        
        else:
            self.blacktime -= change
            if self.blacktime <= 0:
                self.gameover = True
                self.winner = "Red"
    
    def drawtimer(self):
        redtext = self.font.render(f"Red: {int(self.redtime)}", True, Red)
        blacktext = self.font.render(f"Black: {int(self.blacktime)}", True, Black)
        self.screen.blit(redtext, (20, 820))
        self.screen.blit(blacktext, (620, 820))
    
    #User selction 
    def select(self, row, col):
        if self.gameover:
            return
        Piece = self.board[row][col]
        if self.selected:
            if self.validmove(self.selected, row, col):
                self.board.movepiece(self.selected, row, col)
                self.changeturn()
            self.selected = None 
        else:
            if Piece and Piece.color == self.turn:
                self.selcted = Piece
    
    def validmove(self, piece, row, col):
        if self.board.grid[row][col] is not None:
            return False
        