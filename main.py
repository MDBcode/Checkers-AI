import pygame
from stuffs.constants import WIDTH, HEIGHT, SQUARE_SIZE, BLUE, RED
from stuffs.game import Game
from stuffs.board import Board
from minimax.algorithm import minimax

FPS = 60
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SahDama")


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y//SQUARE_SIZE
    col = x//SQUARE_SIZE
    return row, col


def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(window)

    while run:
        clock.tick(FPS)

        if game.turn == RED:
            value, new_board = minimax(
                game.get_board(), 3, float('-inf'), float('inf'), RED, game)
            game.ai_move(new_board)

        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
        game.update()

    pygame.quit()


main()
