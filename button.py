"""
Contains the button class.
"""

import pygame.mouse


class Button(pygame.sprite.Sprite):
    """
    Clickable item in screen. Changes image when mouse is hovered on top of it.
    """

    def __init__(self, x, y, default_image, hovered_image=None, *groups):
        super().__init__(*groups)
        self.default_image = default_image
        self.hovered_image = default_image if hovered_image is None else hovered_image
        self.image = default_image
        self.rect = self.default_image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def update(self):
        self.image = self.hovered_image if self.is_hovered() else self.default_image

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self):
        return self.is_hovered() and pygame.mouse.get_pressed(3)[0]
