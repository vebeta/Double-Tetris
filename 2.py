import pygame

from random import randint
from objects import Board, Shape, Cell
from methods import random_shape


test_field = '''0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
                0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
                0 0 0 0 0 0 1 1 1 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'''

if __name__ == '__main__':
    pygame.init()
    size = X, Y = 501, 501
    screen = pygame.display.set_mode(size)

    running = True

    board = Board(15, 15, screen, test_field)
    board.set_view(50, 50, 30)

    current_shape = random_shape(board, 2, 0, 6)
    is_moved = False
    v = 30
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

        if down_move and cur_iter % 3:
            current_shape.move(2)

        if right_move and not cur_iter % 3:
            current_shape.move(1)

        if left_move and not cur_iter % 3:
            current_shape.move(3)

        if up_move and not cur_iter % 3:
            current_shape.move(0)

        if cur_iter == v:
            cur_iter = 0
            if not current_shape or current_shape.move() is False:
                print(is_moved)
                if not is_moved:
                    assert False, 'Функция для поражения'
                if current_shape:
                    current_shape.stop_shape()
                    current_shape = None
                if board.check():
                    pass
                else:
                    is_moved = False
                    side = (side + 1) % 4
                    if side == 0:
                        current_shape = random_shape(board, 2, 0, 6)
                    elif side == 1:
                        current_shape = random_shape(board, 3, 6, 12)
                    elif side == 2:
                        current_shape = random_shape(board, 0, 12, 6)
                    elif side == 3:
                        current_shape = random_shape(board, 1, 6, 0)
                    down_move = False
                    up_move = False
                    right_move = False
                    left_move = False
            else:
                is_moved = True
        board.update_field()
        board.render()
        pygame.display.flip()

        clock.tick(fps)

        cur_iter += 1

    pygame.quit()
