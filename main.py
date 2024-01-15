







































































































































































































import  pygame
import sys
from just_classes import Button


pygame.init()

WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Double Tetris")

main_background = pygame.image.load("bg_main_menu.png")

def start_window():
    buttons = []

    start_button = Button(WIDTH // 2 - 125, 200, 250, 70, "Начать игру", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(start_button)
    levels_button = Button(WIDTH // 2 - 125, 280, 250, 70, "Уровни", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(levels_button)
    records_button = Button(WIDTH // 2 - 125, 360, 250, 70, "Рекорды", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(records_button)
    settings_button = Button(WIDTH // 2 - 125, 440, 250, 70, "Настройки", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(settings_button)
    exit_button = Button(WIDTH // 2 - 125, 520, 250, 70, "Выйти", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(exit_button)

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (0, 0))

        font = pygame.font.Font(None, 100)
        text = font.render("Double Tetris!", True, (255, 0, 0))
        text_x = (WIDTH - text.get_width()) // 2
        text_y = (HEIGHT - text.get_height()) // 6
        screen.blit(text, (text_x, text_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_window()
            if event.type == pygame.USEREVENT and event.button == start_button:
                game_window()
            for but in buttons:
                but.process_events(event)
        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

def game_window():
    buttons = []

    restart_button = Button(410, 370, 250, 40, "Начать заново", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(restart_button)
    pause_button = Button(410, 430, 200, 40, "Пауза", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(pause_button)
    settings_button = Button(410, 490, 200, 40, "Настройки", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(settings_button)
    exit_button = Button(410, 550, 200, 40, "Выйти", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(exit_button)

    running = True
    while running:
        screen.fill((0, 0, 0))

        pygame.draw.line(screen, (255, 255, 255), (400, 0), (400, 600))

        font = pygame.font.Font(None, 50)
        text = font.render("Жизни", True, (255, 255, 255))
        text_x = 405
        text_y = 10
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 50)
        text = font.render("Сложность", True, (255, 255, 255))
        text_x = 405
        text_y = 50
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 50)
        text = font.render("Лучший результат", True, (255, 255, 255))
        text_x = 405
        text_y = 90
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 50)
        text = font.render("Таймер", True, (255, 255, 255))
        text_x = 405
        text_y = 130
        screen.blit(text, (text_x, text_y))

        font = pygame.font.Font(None, 50)
        text = font.render("Следующая фигура", True, (255, 255, 255))
        text_x = 405
        text_y = 170
        screen.blit(text, (text_x, text_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
            if event.type == pygame.USEREVENT and event.button == settings_button:
                settings_window()
            for but in buttons:
                but.process_events(event)
        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()
    pygame.quit()
    sys.exit()

def settings_window():
    buttons = []

    easy_button = Button(WIDTH // 2 - 125, 200, 250, 70, "Легко", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(easy_button)
    norm_button = Button(WIDTH // 2 - 125, 280, 250, 70, "Нормально", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(norm_button)
    hard_button = Button(WIDTH // 2 - 125, 360, 250, 70, "Сложно", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(hard_button)
    exit_button = Button(WIDTH // 2 - 125, 480, 250, 70, "Назад", "base_button_bg.jpg", sound_path="start_sound.mp3")
    buttons.append(exit_button)
    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(main_background, (-800, 0))

        font = pygame.font.Font(None, 100)
        text = font.render("СЛОЖНОСТЬ", True, (255, 0, 0))
        text_x = (WIDTH - text.get_width()) // 2
        text_y = (HEIGHT - text.get_height()) // 6
        screen.blit(text, (text_x, text_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT and event.button == exit_button:
                running = False
            for but in buttons:
                but.process_events(event)
        for but in buttons:
            but.check_triggered(pygame.mouse.get_pos())
            but.draw(screen)
        pygame.display.flip()

def records_table_window():
    pass

if __name__ == "__main__":
    start_window()