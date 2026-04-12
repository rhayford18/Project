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
        
        row_diff = row - piece.row
        col_diff = abs(col - piece.col)
        direction = -1 if piece.color == Red else 1

        #regular player movememnt
        if row_diff == direction and col_diff == 1:
            return True
        
        #Player vs Player caputre 
        if row_diff == 2 * direction and col_diff == 2:
            jumped_row = piece.row + direction 
            jumped_col = (piece.col + col) // 2
            jumped_piece = self. board. grid[jumped_row][jumped_col]
            if jumped_piece and jumped_piece.color != piece.color:
                self.board.remove_piece(jumped_row, jumped_col)
                return True 

        return False 

    def change_turn(self):
        self.turn + Black if self.turn == Red else Red
        self.last_tick = pygame.time.get_ticks()

    def draw_gameover(self):
        text = self.font.render(f"{self.winner} wins!", True, White)
        self.screen.blit(text, (Width // 2 - 120, Height // 2)) 

    def draw(self):
        self.board.draw(self.screen)
        self.drawtimer()

        if self.selcted:
            pygame.draw.rect(
                self.screen,
                Blue,
                (
                    self.selected.col * Size,
                    self.selcted.row * Size,
                    Size,
                    Size
                ),
                3
            ) 
        if self.gameover:
            self.draw_gameover()
#The Main loop that runs the game 
def main():
    screen = pygame.display.set_mode(Width, Height)
    pygame.display.set_caption("Timed Checkers")
    clock = pygame.time.Clock()

    game = Game()

    running = True 
    while running:
        clock.tick(Fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            if event. type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if y < Width:
                    row = y // Size
                    col = x // Size
                    game.select(row, col)
        if not game.gameover:
            game.updatetimer()

        screen .fill(0, 0, 0)  
        game.draw()
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()           