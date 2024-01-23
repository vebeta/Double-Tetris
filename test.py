import pygame

from random import randint
from objects import Board, Shape, Cell
from methods import random_shape


test_field = '''0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0
                1 1 1 1 1 1 1 1 1 1'''

if __name__ == '__main__':
    pygame.init()
    size = X, Y = 501, 501
    screen = pygame.display.set_mode(size)

    running = True

    board = Board(10, 10, screen, test_field)
    board.set_view(50, 50, 30)

    current_shape = random_shape(board, 2, 0, 4)
    v = 30
    cur_iter = 0
    fps = 30
    clock = pygame.time.Clock()
    while running:
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                current_shape.move(1)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                current_shape.move(3)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                current_shape.move(2)

        if cur_iter == v:
            cur_iter = 0
            if current_shape.move() is False:
                board.check()
                current_shape = random_shape(board, 2, 0, 4)
        board.update_field()
        board.render()
        pygame.display.flip()

        clock.tick(fps)

        cur_iter += 1

    pygame.quit()
