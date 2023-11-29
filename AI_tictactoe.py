import sys
import pygame
import copy
import numpy as np
import random


from constants import * #imports everything
#PYGAME SET UP
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TIC TAC TOE GAME")
screen.fill(BG_COLOUR)


class Board:
    def __init__(self):
        self.squares = np.zeros((ROWS,COLS))  #2D Array similar to C 
        self.empty_board = self.squares  
        self.number_of_marks_on_board = 0

    def final_state(self):

        #return 0 = no win yet
        #return 1 = player1 wins
        #return 2 = player2 wins
        
        #check for any vertical wins
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares [2][col] != 0:
                return self.squares[0][col]
        
        #check for any horizontal wins
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares [row][2] != 0:
                return self.squares[row][0]
            
        #check for descending diagonal wins
        if self.squares[0][0] == self.squares[1][1] == self.squares [2][2] != 0:
            return self.squares[0][0]
        
        #check for ascending diagonal wins
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[2][0]
        
        #no win yet
        return 0

    def mark_square(self, row, col, player):
        self.squares[row][col] = player
        self.number_of_marks_on_board += 1
    
    def empty_squares(self, row, col):
        return self.squares[row][col] == 0
    
    def get_empty_squares(self):
        empty_squares = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_squares(row, col) == True:
                    empty_squares.append((row,col))
        return empty_squares
    
    def is_full(self):
        return self.number_of_marks_on_board == 9
            
    def is_empty(self):
        return self.number_of_marks_on_board == 0
    
class AI:
    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    def random_choice(self, board):
        empty_squares = board.get_empty_squares()
        index = random.randrange(0, len(empty_squares))

        return empty_squares[index]
    
    def minimax(self, board, maximizing):
        case = board.final_state()

        if case == 1:
            return 1, None
        
        if case == 2:
            return -1, None
        
        elif board.is_full():
            return 0, None
        
        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col , 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row,col)
            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_squares()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_square(row, col , self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row,col)
            return min_eval, best_move


    def eval(self, main_board):
        if self.level == 0:
            eval = 'random'
            move = self.random_choice(main_board)
        else:
           eval, move = self.minimax(main_board, False)

        print("AI has chosen to mark the square in pos",move,"with an eval of",eval)

        return move

class Game:
    def __init__(self):
        self.board = Board()
        self.player = 1 #Player1: X   Player2: O
        self.ai = AI()
        self.gamemode = 'ai' #pvp or ai
        self.running = True
        self.show_lines()    
    
    
    def make_move(self, row, col):
        self.board.mark_square(row, col, self.player)
        self.draw_figure(row, col)
        self.next_player()

    def show_lines(self):
        #Vertical lines
        pygame.draw.line(screen, LINE_COLOUR, (SQUARE_SIZE,0),(SQUARE_SIZE,HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (WIDTH-SQUARE_SIZE,0),(WIDTH-SQUARE_SIZE,HEIGHT), LINE_WIDTH)

        #Horizontal lines
        pygame.draw.line(screen, LINE_COLOUR, (0,SQUARE_SIZE),(HEIGHT,SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOUR, (0,WIDTH-SQUARE_SIZE),(HEIGHT,WIDTH-SQUARE_SIZE), LINE_WIDTH)

    def next_player(self):
        self.player = (self.player%2) + 1 #Changes player from 1 to 2 AND 2 to 1

    def draw_figure(self, row, col):
        if self.player == 1:
            start_desc = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + OFFSET)
            end_desc = (col * SQUARE_SIZE + SQUARE_SIZE-OFFSET, row * SQUARE_SIZE + SQUARE_SIZE-OFFSET)
            
            start_ascen = (col * SQUARE_SIZE + OFFSET, row * SQUARE_SIZE + SQUARE_SIZE - OFFSET)
            end_ascen = (col * SQUARE_SIZE + SQUARE_SIZE-OFFSET, row * SQUARE_SIZE + OFFSET)
            
            pygame.draw.line(screen, CROSS_COLOUR, start_desc, end_desc, CROSS_WIDTH)
            pygame.draw.line(screen, CROSS_COLOUR, start_ascen, end_ascen, CROSS_WIDTH)


        elif self.player == 2:
            center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row*SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(screen,CIRCLE_COLOUR, center, RADIUS, CIRCLE_WIDTH)     




#Main game loop, keeps screen up and when user quits it closes the window
def main():

    game = Game()
    board = game.board
    ai = game.ai

#MAIN loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQUARE_SIZE
                col = pos[0] // SQUARE_SIZE
                if board.empty_squares(row, col) == True and game.running:
                    game.make_move(row, col)
                  
                else:
                    print("Invalid move")

        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            
            pygame.display.update()
            pygame.time.delay(400)

            row, col = ai.eval(board)
            game.make_move(row, col)
            

          
        pygame.display.update()
main()
