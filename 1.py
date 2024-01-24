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
    size = X, Y = 1001, 701
    screen = pygame.display.set_mode(size)

    running = True

    board = Board(10, 15, screen, test_field)
    board.set_view(50, 50, 30)

    current_shape = random_shape(board, 2, 0, 6)
    v = 30
    moving_shapes = False
    down_move = False
    right_move = False
    left_move = False
    up_move = False
    cur_iter = 0
    fps = 30
    side = 0
    clock = pygame.time.Clock()
    while running:
        screen.fill('black')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                if current_shape.direction == 3:
                    current_shape.rotate()
                else:
                    right_move = True

            if event.type == pygame.KEYUP and event.key == pygame.K_RIGHT:
                right_move = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                if current_shape.direction == 1:
                    current_shape.rotate()
                else:
                    left_move = True

            if event.type == pygame.KEYUP and event.key == pygame.K_LEFT:
                left_move = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                if current_shape.direction == 0:
                    current_shape.rotate()
                else:
                    down_move = True

            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                down_move = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                if current_shape.direction == 2:
                    current_shape.rotate()
                else:
                    up_move = True

            if event.type == pygame.KEYUP and event.key == pygame.K_UP:
                up_move = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                current_shape.rotate()

        # print(left_move, right_move, up_move, down_move)

        if down_move and not cur_iter % 3:
            current_shape.move(2)

        if right_move and not cur_iter % 3:
            current_shape.move(1)

        if left_move and not cur_iter % 3:
            current_shape.move(3)

        if up_move and not cur_iter % 3:
            current_shape.move(0)

        if cur_iter == v:
            cur_iter = 0
            if not current_shape or (act := current_shape.move()) is False or act == 'lose':
                if act == 'lose':
                    assert False, 'Функция для поражения'
                if current_shape:
                    current_shape.stop_shape()
                    current_shape = None
                n = board.check()
                if n or moving_shapes:
                    try:
                        moving_shapes = board.move_shapes()
                        pass
                    except IndexError:
                        assert False, 'Функция для поражения'
                else:
                    current_shape = random_shape(board, 2, 0, 6)
                    down_move = False
                    up_move = False
                    right_move = False
                    left_move = False
        try:
            board.update_field()
        except IndexError:
            assert False, 'Функция для поражения'
        board.render()
        pygame.display.flip()

        clock.tick(fps)

        cur_iter += 1

    pygame.quit()