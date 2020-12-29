import pygame

BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
YELLOW = (255, 165, 0)
RED = (200, 0, 0)


def give_delay():
    pygame.time.wait(500)


class Draw:
    _square: int
    _radius: int
    _column: int
    _row: int

    def __init__(self, board):
        self._square = 100
        self._radius = 42
        self._column = len(board[0])
        self._row = len(board)

    def getSquare(self):
        return self._square

    def draw_board(self):
        width = self._square * self._column
        height = self._square * (self._row + 1)
        screen = pygame.display.set_mode((width, height))
        pygame.init()
        for r in range(0, self._row):
            for c in range(0, self._column):
                pygame.draw.rect(screen, BLUE, (self._square * c,
                                                self._square * (r + 1),
                                                self._square, self._square))
                pygame.draw.circle(screen, BLACK, (self._square * c +
                                                   self._square / 2,
                                                   self._square * (
                                                           r + 1.5)), 42)
        pygame.display.update()

    def update_board(self, board):
        screen = pygame.display.get_surface()
        for r in range(0, len(board)):
            for c in range(0, len(board[0])):
                pygame.draw.rect(screen, BLUE, (self._square * c,
                                                self._square * (r + 1),
                                                self._square, self._square))
                if board[r][c] == 1:
                    color = RED
                elif board[r][c] == 2:
                    color = YELLOW
                else:
                    color = BLACK
                pygame.draw.circle(screen, color, (self._square * c +
                                                   self._square / 2,
                                                   self._square * (
                                                           r + 1.5)), 42)
        pygame.display.update()

    def draw_hover(self, pos: int, turn: int):
        screen = pygame.display.get_surface()

        if turn == 1:
            color = RED
        else:
            color = YELLOW

        pygame.draw.rect(screen, BLACK, (0, 0, self._square * self._column, self._square))
        pygame.draw.circle(screen, color, (pos, self._square/2), self._radius)
        pygame.display.update()

    def display_game_over(self, turn: int):
        screen = pygame.display.get_surface()
        pygame.draw.rect(screen, BLACK, (0, 0, self._square * self._column, self._square))
        if turn == 1:
            color = RED
        else:
            color = YELLOW

        my_font = pygame.font.SysFont('monospace', 75)
        label = my_font.render("Player" + str(turn) + " wins!", 2, color)
        screen.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(3000)
