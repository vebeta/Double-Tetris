import pygame
import sys

from Button import Button
from game_functoins import display_text
from objects import Board
from methods import random_shape

pygame.init()

WIDTH, HEIGHT = 1000, 600
FONT = "FRM325x8.ttf"
lives = 3
diff = "Легко"
time_triggers = {"Легко": 30,
                 "Нормально": 60,
                 "Сложно": 120}

curr_level = '1'
level_fields = {'1': '''0 0 0 0 0 0 0 0 0 0
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
                1 1 1 1 1 1 1 1 1 1''',
                '2': '''0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
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
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0''',
                '3': '''0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 1 1 1 1 1 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
                0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0'''}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Tetris")

clock = pygame.time.Clock()
fps = 30

sound_flag = True


def start_window():
    main_background = pygame.image.load("main_bg.jpg")
    main_background = pygame.transform.scale(main_background, (WIDTH, HEIGHT))

    buttons = []
    btn_width, btn_height = 250, 70

    start_button = Button(WIDTH // 2 - 125, 160, btn_width, btn_height, "Начать игру", "button_bg.png", font_path=FONT,
                          sound_path="start_sound.mp3")
    buttons.append(start_button)
    levels_button = Button(WIDTH // 2 - 125, 240, btn_width, btn_height, "Уровни", "button_bg.png", font_path=FONT,
                           sound_path="start_sound.mp3")
    buttons.append(levels_button)
    settings_button = Button(WIDTH // 2 - 125, 320, btn_width, btn_height, "Настройки", "button_bg.png", font_path=FONT,
                             sound_path="start_sound.mp3")
    buttons.append(settings_button)
    exit_button = Button(WIDTH // 2 - 125, 500, btn_width, btn_height, "Выйти", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(exit_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))

        font = pygame.font.Font(FONT, 100)
        text = font.render("Double Tetris!", True, (255, 0, 0))
        text_x = (WIDTH - text.get_width()) // 2
        text_y = (HEIGHT - text.get_height()) // 10
        screen.blit(text, (text_x, text_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
            if event.type == pygame.USEREVENT and event.button == start_button:
                game_window()
            if event.type == pygame.USEREVENT and event.button == levels_button:
                levels_window()
            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_window()
            for but in buttons:
                but.process_events(event, sound_flag)
        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
    sys.exit()


def game_window():
    global lives

    hours = mints = scnds = mil_scnds = 0

    buttons = []

    restart_button = Button(530, 410, 200, 55, "Заново", "button_bg.png", font_path=FONT,
                            sound_path="start_sound.mp3")
    buttons.append(restart_button)
    settings_button = Button(WIDTH - 220, 410, 200, 55, "Настройки", "button_bg.png", font_path=FONT,
                             sound_path="start_sound.mp3")
    buttons.append(settings_button)
    pause_button = Button(530, 475, 200, 55, "Пауза", "button_bg.png", font_path=FONT, sound_path="start_sound.mp3")
    buttons.append(pause_button)
    back_button = Button(WIDTH - 220, 475, 200, 55, "Назад", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(back_button)
    exit_button = Button(WIDTH * 3 // 4 - 100, 540, 200, 55, "Выйти", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(exit_button)

    board_size_x, board_size_y, cell_size = 0, 0, 30
    if curr_level == '1':
        board_size_x, board_size_y = 10, 15
        cell_size = 40
    elif curr_level == '2':
        board_size_x, board_size_y = 15, 15
        cell_size = 30
    elif curr_level == '3':
        board_size_x, board_size_y = 21, 16
        cell_size = 25

    current_level_field = level_fields[curr_level]

    board = Board(board_size_x, board_size_y, screen, current_level_field)
    board.set_view(0, 0, cell_size)

    if curr_level == '1' or curr_level == '2':
        current_shape = random_shape(board, 2, 0, 6)
    elif curr_level == '3':
        current_shape = random_shape(board, 2, 0, 10)
    v = 30
    moving_shapes = False
    down_move = False
    right_move = False
    left_move = False
    up_move = False
    cur_iter = 0
    side = 0

    running = True
    while running:

        screen.fill((0, 0, 0))

        pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2 + 24, 0), (WIDTH // 2 + 24, 600))

        display_text(screen, f"Жизни:  {lives}", WIDTH // 2 + 25, 10, text_size=30)

        display_text(screen, f"Сложность:  {diff}", WIDTH // 2 + 25, 50, text_size=30)

        display_text(screen, "Рекорд:  --", WIDTH // 2 + 25, 90, text_size=30)

        display_text(screen, "Таймер:   {}:{}:{}".format(hours, mints, scnds), WIDTH // 2 + 25, 130, text_size=30)

        mil_scnds += 1
        if mil_scnds == time_triggers[diff]:
            scnds += 1
            mil_scnds = 0
        if scnds == time_triggers[diff]:
            mints += 1
            scnds = 0
        if mints == time_triggers[diff]:
            hours += 1
            mints = 0

        display_text(screen, "Следующая фигура:", WIDTH // 2 + 25, 170, text_size=30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
                pygame.quit()
                sys.exit()

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

            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
            if event.type == pygame.USEREVENT and event.button == restart_button:
                running = False
                game_window()
            if event.type == pygame.USEREVENT and event.button == pause_button:
                pause_window()
            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_window()
            for but in buttons:
                but.process_events(event, sound_flag)

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
                    running = False
                    if lives > 0:
                        lives -= 1
                        game_window()
                    else:
                        loose_window()
                if current_shape:
                    current_shape.stop_shape()
                    current_shape = None
                n = board.check()
                if n or moving_shapes:
                    try:
                        moving_shapes = board.move_shapes()
                        pass
                    except IndexError:
                        running = False
                        if lives > 0:
                            lives -= 1
                            game_window()
                        else:
                            loose_window()
                else:
                    if curr_level == '1':
                        current_shape = random_shape(board, 2, 0, 6)
                    elif curr_level == '2':
                        side = (side + 1) % 4
                        if side == 0:
                            current_shape = random_shape(board, 2, 0, 6)
                        elif side == 1:
                            current_shape = random_shape(board, 3, 6, 14)
                        elif side == 2:
                            current_shape = random_shape(board, 0, 14, 6)
                        elif side == 3:
                            current_shape = random_shape(board, 1, 6, 0)
                    elif curr_level == '3':
                        side = (side + 1) % 4
                        if side == 0:
                            current_shape = random_shape(board, 2, 0, 10)
                        elif side == 1:
                            current_shape = random_shape(board, 3, 8, 21)
                        elif side == 2:
                            current_shape = random_shape(board, 0, 16, 10)
                        elif side == 3:
                            current_shape = random_shape(board, 1, 8, 0)
                    down_move = False
                    up_move = False
                    right_move = False
                    left_move = False
        try:
            board.update_field()
        except IndexError:
            running = False
            if lives > 1:
                lives -= 1
                game_window()
            else:
                loose_window()
        board.render()

        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
        cur_iter += 1


def settings_window():
    settings_background = pygame.image.load("settings_bg.jpg")
    settings_background = pygame.transform.scale(settings_background, (WIDTH, HEIGHT))

    buttons = []

    difficulty_button = Button(WIDTH // 2 - 125, 200, 250, 70, "Сложность", "button_bg.png", font_path=FONT,
                               sound_path="start_sound.mp3")
    buttons.append(difficulty_button)
    audio_button = Button(WIDTH // 2 - 125, 280, 250, 70, "Аудио", "button_bg.png", font_path=FONT,
                          sound_path="start_sound.mp3")
    buttons.append(audio_button)
    back_button = Button(WIDTH // 2 - 125, 480, 250, 70, "Назад", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(back_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(settings_background, (0, 0))

        font = pygame.font.Font(FONT, 100)
        text = font.render("Настройки", True, (255, 0, 0))
        text_x = (WIDTH - text.get_width()) // 2
        text_y = (HEIGHT - text.get_height()) // 8
        screen.blit(text, (text_x, text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
            if event.type == pygame.USEREVENT and event.button == difficulty_button:
                difficulty_settings_window()
            if event.type == pygame.USEREVENT and event.button == audio_button:
                audio_settings_window()
            for but in buttons:
                but.process_events(event, sound_flag)
        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def difficulty_settings_window():
    global sound_flag, lives, diff, fps
    difficulty_stngs_bg = pygame.image.load("settings_bg_2.jpg")
    difficulty_stngs_bg = pygame.transform.scale(difficulty_stngs_bg, (WIDTH, HEIGHT))

    buttons = []

    easy_button = Button(WIDTH // 5 - 125, 200, 250, 70, "Легко", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(easy_button)
    medium_button = Button(WIDTH // 2 - 125, 200, 250, 70, "Нормально", "button_bg.png", font_path=FONT,
                           sound_path="start_sound.mp3")
    buttons.append(medium_button)
    hard_button = Button(WIDTH // 5 * 4 - 125, 200, 250, 70, "Сложно", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(hard_button)
    back_button = Button(WIDTH // 2 - 125, 290, 250, 70, "Назад", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(back_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(difficulty_stngs_bg, (0, 0))

        font = pygame.font.Font(FONT, 70)
        text = font.render("Настройки Сложности", True, (255, 0, 0))
        text_x = (WIDTH - text.get_width()) // 2
        text_y = (HEIGHT - text.get_height()) // 6
        screen.blit(text, (text_x, text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == easy_button:
                lives = 3
                fps = 30
                diff = "Легко"
            if event.type == pygame.USEREVENT and event.button == medium_button:
                lives = 2
                fps = 60
                diff = "Нормально"
            if event.type == pygame.USEREVENT and event.button == hard_button:
                lives = 1
                fps = 120
                diff = "Сложно"
            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
            for but in buttons:
                but.process_events(event, sound_flag)
        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def audio_settings_window():
    global sound_flag
    audio_stngs_bg = pygame.image.load("settings_bg_2.jpg")
    audio_stngs_bg = pygame.transform.scale(audio_stngs_bg, (WIDTH, HEIGHT))

    buttons = []

    sound_on_button = Button(WIDTH // 5 - 125, 200, 250, 70, "Включить", "button_bg.png", font_path=FONT,
                             sound_path="start_sound.mp3")
    buttons.append(sound_on_button)
    sound_off_button = Button(WIDTH // 2 - 125, 200, 250, 70, "Отключить", "button_bg.png", font_path=FONT,
                              sound_path="start_sound.mp3")
    buttons.append(sound_off_button)
    back_button = Button(WIDTH // 5 * 4 - 125, 200, 250, 70, "Назад", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(back_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(audio_stngs_bg, (0, 0))

        font = pygame.font.Font(FONT, 70)
        text = font.render("Настройки Звука", True, (255, 0, 0))
        text_x = (WIDTH - text.get_width()) // 2
        text_y = (HEIGHT - text.get_height()) // 8
        screen.blit(text, (text_x, text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == sound_on_button:
                sound_flag = True
            if event.type == pygame.USEREVENT and event.button == sound_off_button:
                sound_flag = False
            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
            for but in buttons:
                but.process_events(event, sound_flag)
        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def levels_window():
    global sound_flag, curr_level
    levels_bg = pygame.image.load("levels_bg.jpg")
    levels_bg = pygame.transform.scale(levels_bg, (WIDTH, HEIGHT))

    buttons = []

    level1_button = Button(WIDTH // 5 - 125, 200, 250, 70, "Уровень 1", "button_bg.png", font_path=FONT,
                           sound_path="start_sound.mp3")
    buttons.append(level1_button)
    level2_button = Button(WIDTH // 2 - 125, 200, 250, 70, "Уровень 2", "button_bg.png", font_path=FONT,
                           sound_path="start_sound.mp3")
    buttons.append(level2_button)
    level3_button = Button(WIDTH // 5 * 4 - 125, 200, 250, 70, "Уровень 3", "button_bg.png", font_path=FONT,
                           sound_path="start_sound.mp3")
    buttons.append(level3_button)
    back_button = Button(WIDTH // 2 - 125, 310, 250, 70, "Назад", "button_bg.png", font_path=FONT,
                         sound_path="start_sound.mp3")
    buttons.append(back_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(levels_bg, (0, 0))

        font = pygame.font.Font(FONT, 70)
        text = font.render("Выбор уровня", True, (255, 0, 0))
        text_x = (WIDTH - text.get_width()) // 2
        text_y = (HEIGHT - text.get_height()) // 6
        screen.blit(text, (text_x, text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == level1_button:
                curr_level = '1'
                game_window()
            if event.type == pygame.USEREVENT and event.button == level2_button:
                curr_level = '2'
                game_window()
            if event.type == pygame.USEREVENT and event.button == level3_button:
                curr_level = '3'
                game_window()
            if event.type == pygame.USEREVENT and event.button == back_button:
                running = False
            for but in buttons:
                but.process_events(event, sound_flag)
        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def pause_window():
    pause = True

    back_pause_button = Button(WIDTH // 2 - 150, HEIGHT // 2 - 35, 300, 84, "Вернуться в игру", "button_bg.png",
                               font_path=FONT, sound_path="start_sound.mp3")

    while pause:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == back_pause_button:
                pause = False
            back_pause_button.process_events(event, sound_flag)
        back_pause_button.check_triggered(pygame.mouse.get_pos())
        back_pause_button.draw(screen)
        pygame.display.flip()
        clock.tick(fps)


def loose_window():
    running = True

    return_button = Button(WIDTH // 2 - 50, HEIGHT // 2 - 35, 100, 84, "ОК", "button_bg.png",
                           font_path=FONT, sound_path="start_sound.mp3", text_size=40)

    while running:
        screen.fill((0, 0, 0))

        display_text(screen, "Вы проиграли", WIDTH // 3, 50, text_size=40)
        display_text(screen, "Возможно вы нарушили правила (не делайте так)", 30, 130, text_size=30)
        display_text(screen, "Нажмите ОК для возвращения в главное меню", 50, 200, text_size=30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == return_button:
                running = False
            return_button.process_events(event, sound_flag)
        return_button.check_triggered(pygame.mouse.get_pos())
        return_button.draw(screen)
        pygame.display.flip()
        clock.tick(fps)
