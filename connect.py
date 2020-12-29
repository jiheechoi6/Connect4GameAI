import random
import sys
from pygame import *
import math
from graphics import *
from game import *

COLUMN = 7
ROW = 6
HUMAN = 1
AI = 2

game_over = False
turn = random.randint(HUMAN, AI)

game = Game(ROW, COLUMN)
graphic = Draw(game.get_board())
graphic.draw_board()

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            pos_x = int(math.floor(event.pos[0]))
            graphic.draw_hover(pos_x, turn)
        if event.type == pygame.MOUSEBUTTONDOWN:
            selection = int(math.floor(event.pos[0] / graphic.getSquare()))

            if selection not in range(0, COLUMN):
                print("you have made an invalid selection. Try again")
            elif not game.is_location_valid(selection):
                print("This column is already full")
            else:
                row = game.get_available_row(None, selection)
                board = game.make_move(row, selection, turn)
                graphic.update_board(game.get_board())
                if game.is_there_winner(None) == HUMAN:
                    graphic.update_board(game.get_board())
                    graphic.display_game_over(turn)
                    game_over = True
                    break
                turn = AI

    if turn == AI:
        # col = random.randint(0, COLUMN-1)
        col = game.pick_best_move(AI)
        row = game.get_available_row(None, col)
        game.make_move(row, col, turn)
        give_delay()
        graphic.update_board(game.get_board())
        if game.is_there_winner(None) == AI:
            graphic.update_board(game.get_board())
            graphic.display_game_over(turn)
            game_over = True
            break
        turn = HUMAN
