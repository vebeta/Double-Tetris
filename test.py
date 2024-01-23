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

    board = Board(10, 15, screen, test_field)
    board.set_view(50, 50, 30)

    current_shape = random_shape(board, 2, 0, 4)
    is_moved = False
    v = 30
    fast_down = False
    right_move = False
    left_move = False
    cur_iter = 0
    fps = 30
    clock = pygame.time.Clock()
    while running:
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                right_move = True

            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right_move = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                left_move = True

            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left_move = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                fast_down = True

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                fast_down = False

            if event.type == pygame.KEYDOWN and (event.key == pygame.K_UP or event.key == pygame.K_SPACE):
                current_shape.rotate()

        if fast_down and cur_iter % 2:
            current_shape.move(2)

        if right_move and not cur_iter % 3:
            current_shape.move(1)

        if left_move and not cur_iter % 3:
            current_shape.move(3)

        if cur_iter == v:
            cur_iter = 0
            if not current_shape or current_shape.move() is False:
                if not is_moved:
                    assert(False, 'Функция для поражения')
                if current_shape:
                    current_shape.stop_shape()
                    current_shape = None
                if board.check():
                    pass
                else:
                    current_shape = random_shape(board, 2, 0, 4)
                    fast_down = False
                    right_move = False
                    left_move = False
        board.update_field()
        board.render()
        pygame.display.flip()

        clock.tick(fps)

        cur_iter += 1

    pygame.quit()
