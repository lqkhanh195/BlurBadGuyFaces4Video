import pygame
from pygame.locals import *

color = {
    'white': (255, 255, 255),
    'bright_white': (255, 255, 200),
    'red': (200,0,0),
    'bright_red': (255,0,0),
}

class Screen:
    def __init__(self, btns, bg_img = None, w = 612, h = 480):
        self.__bg = bg_img
        self.__btns = btns
    def display(self, display_surf):
        if self.__bg is not None:
            display_surf.blit(self.__bg, (0, 0))

        for btn in self.__btns:
            btn.display(display_surf)

class Button:
    def __init__(self, x, y, w, h, color, text, mouse_pos, click):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__color = color
        self.__mouse_pos = mouse_pos
        self.__click = click
        self.__text = text
    def update_mouse_pos(self, mousepos):
        self.__mouse_pos = mousepos
    def update_click(self, click):
        self.__click = click
    def is_clicked(self):
        if  self.__mouse_pos is not None:
            if self.__x + self.__w > self.__mouse_pos[0] > self.__x\
                and self.__y + self.__h > self.__mouse_pos[1] > self.__y:
                if self.__click[0] == True:
                    return True
    def display(self, display_surf):
        if self.__mouse_pos is not None:
            if self.__x + self.__w > self.__mouse_pos[0] > self.__x\
                and self.__y + self.__h > self.__mouse_pos[1] > self.__y:
                pygame.draw.rect(display_surf, color['bright_' + self.__color], (self.__x, self.__y, self.__w, self.__h), 0)
            else:
                pygame.draw.rect(display_surf, color[self.__color], (self.__x, self.__y, self.__w, self.__h), 0)

            if self.__text is not None:
                font = pygame.font.Font(None, 40)
                button_text = font.render(self.__text, True, (0, 0, 0))
                button_text_rect = button_text.get_rect(center=(self.__x + self.__w/2, self.__y + self.__h/2))
                display_surf.blit(button_text, button_text_rect)
    def button_func(self):
        return True