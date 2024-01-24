import pygame


def display_text(screen, text, x, y, text_color=(255, 255, 255), font="FRM325x8.ttf", text_size=40):
    font = pygame.font.Font(font, text_size)
    text = font.render(text, True, text_color)
    text_x = x
    text_y = y
    screen.blit(text, (text_x, text_y))


def loose(livs):
    if livs > 0:
        livs -= 1
    elif livs <= 0:
        return False