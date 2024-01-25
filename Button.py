import pygame


class Button():
    def __init__(self, x, y, width, height, text, image_path, trig_image_path=None, font_path=None, sound_path=None, text_size=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = font_path
        self.text_size = self.width // self.height * 9
        if text_size is not None:
            self.text_size = text_size

        self.is_triggered = False
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.trig_image = self.image
        if trig_image_path:
            self.trig_image = pygame.image.load(trig_image_path)
            self.trig_image = pygame.transform.scale(self.trig_image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.sound = pygame.mixer.Sound(sound_path) if sound_path else None

    def draw(self, screen):
        current_image = self.trig_image if self.is_triggered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(self.font, self.text_size)
        text = font.render(self.text, True, (0, 0, 0))
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

    def check_triggered(self, mouse_pos):
        self.is_triggered = self.rect.collidepoint(mouse_pos)

    def process_events(self, event, sound_flag):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_triggered:
            if self.sound and sound_flag:
                self.sound.play()
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))