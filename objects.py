import pygame


class Shape(pygame.sprite.Sprite):
    def __init__(self, struct: list, color: tuple, direction: int, *group: pygame.sprite.Group):
        super.__init__(*group)
        self.struct = struct
        self.color = color
        self.direction = direction

    def
