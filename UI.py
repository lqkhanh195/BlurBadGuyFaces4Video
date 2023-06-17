import pygame
from pygame.locals import *
import time
import glob
import os, os.path
import cv2
from tkinter.filedialog import *
from tkinter import *

# Browse file
root = Tk()
root.withdraw()
foo = askopenfilename()
root.destroy()
print(foo)

pygame.init()

for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                flag = True

w = 612
h = 480

display_surf = pygame.display.set_mode((w, h))
pygame.display.set_caption("LetsBlurYourFace")

bg_img = pygame.image.load("imgs\mainBG.jpg").convert_alpha()

fps_clock = pygame.time.Clock()

is_running = True

class Button:
    def __init__(self, x, y, w, h, func, mouse_pos, click, text):
        self.__x = x
        self.__y = y
        self.__w = w
        self.__h = h
        self.__func = func
        self.__mouse_pos = mouse_pos
        self.__click = click
        self.__text = text
        
    def update_mousepos(self, new_mouse_pos):
        self.__mouse_pos = new_mouse_pos
    def display(self):
        if self.__x + self.__w > self.__mouse_pos[0] > self.__x\
            and self.__y + self.__h > self.__mouse_pos[1] > self.__y:
            pygame.draw.rect(display_surf, (255, 255, 200), (self.__x, self.__y, self.__w, self.__h), 0)
            print("int")

            if self.__click[0] == 1:
                self.button_func()
        else:
            pygame.draw.rect(display_surf, (255, 255, 255), (self.__x, self.__y, self.__w, self.__h), 0)

        if self.__text is not None:
            font = pygame.font.Font(None, 40)
            button_text = font.render(self.__text, True, (0, 0, 0))
            button_text_rect = button_text.get_rect(center=(self.__x + self.__w/2, self.__y + self.__h/2))
            display_surf.blit(button_text, button_text_rect)
    def button_func(self):
        return True

mousepos = pygame.mouse.get_pos()
click = pygame.mouse.get_pressed()    
btn = Button(206, 419, 200, 50, None, mousepos, click, "BROWSE")

while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False
            
    mousepos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    btn.update_mousepos(mousepos)
    display_surf.blit(bg_img, (0, 0))
    btn.display()

    pygame.display.update()
    fps_clock.tick(60)

