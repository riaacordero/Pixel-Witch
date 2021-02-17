"""
This module contains strings which locate fonts, and a few classes for rendering fonts and displaying text.
"""

import pygame.font

pygame.font.init()

# Font locations
fff_forward_font = r"assets/font/FFF Forward.ttf"
retro_gaming_font = r"assets/font/Retro Gaming.ttf"


class Text:
    """
    Text shown in screen. Has ability to detect hovers and clicks.
    """

    def __init__(self, x, y, text, font_location, font_size, default_text_color, pos="topleft"):
        self.text = text
        self.font = pygame.font.Font(font_location, font_size)
        self.default_text_color = default_text_color
        self.default_text = self.font.render(text, True, default_text_color)
        self.rect = self.default_text.get_rect()
        self.x, self.y = x, y
        if pos == "topleft":
            self.rect.x, self.rect.y = x, y
        elif pos == "center":
            self.rect.center = x, y
        self.width, self.height = self.default_text.get_width(), self.default_text.get_height()
        self.hovered = False

    def draw(self, screen):
        screen.blit(self.default_text, self.rect)

    def update(self, new_text="", pos="", new_x=-1, new_y=-1):
        self.hovered = self.is_hovered()

        if not new_text == "":
            self.default_text = self.font.render(new_text, True, self.default_text_color)
            self.rect = self.default_text.get_rect()
            self.width, self.height = self.default_text.get_width(), self.default_text.get_height()
            self.rect.x, self.rect.y = self.x, self.y

            if pos == "center":
                self.rect.center = new_x, new_y

    def is_hovered(self):
        mouse_pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self):
        return self.is_hovered() and pygame.mouse.get_pressed(3)[0]


class HoverableText(Text):
    """
    Text that changes appearance when mouse is hovered on it.
    """

    def __init__(self, x, y, text, font_location, font_size, default_text_color, hovered_text_color, hovered_bg_color,
                 pos="topleft"):
        super().__init__(x, y, text, font_location, font_size, default_text_color, pos)
        self.hovered_text_color = hovered_text_color
        self.hovered_text = self.font.render(text, True, hovered_text_color)
        self.hovered_bg_color = hovered_bg_color

    def draw(self, screen):
        if self.hovered:
            pygame.draw.rect(screen, self.hovered_bg_color, self.rect)
            screen.blit(self.hovered_text, self.rect)
        else:
            screen.blit(self.default_text, self.rect)

    def update(self, new_text="", pos="", new_x=0, new_y=0):
        super().update(new_text)
        if not new_text == "":
            self.hovered_text = self.font.render(new_text, True, self.hovered_text_color)


class TextGroup:
    """
    Container for Text and HoverableText objects.
    """

    def __init__(self, *texts: Text):
        self.texts = list(texts)

    def draw(self, screen, *, excluded=()):
        for text in self.texts:
            if text not in excluded:
                text.draw(screen)

    def update(self):
        for text in self.texts:
            text.update()

    def one_is_clicked(self):
        """Returns true if one interactive font is clicked"""
        return any(isinstance(text, HoverableText) and text.is_clicked() for text in self.texts)

    def add(self, *texts):
        self.texts.extend(list(texts))

    def remove(self, *texts):
        for text in texts:
            self.texts.remove(text)
