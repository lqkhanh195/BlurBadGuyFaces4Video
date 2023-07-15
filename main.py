from UI import *
from GetFaceBlurred import *
import GetFaceBlurred as gfp
from tkinter.filedialog import *
from tkinter import messagebox
from tkinter import Tk 
from tkinter import Toplevel, Label
from threading import Thread
import threading
from threading import Thread
#from pyvidplayer import Video

vid_format = ["mp4", "mov", "vmw", "avi", "avchd", "mkv", "mpeg-2"]

class ResultScr(Screen):
    def __init__(self, btns, bg_img = None, w=612, h=480):
        super().__init__(btns, bg_img, w, h)
    def display(self, display_surf):
        return super().display(display_surf)
    
class BrowseBtn(Button):
    def __init__(self, x, y, w, h, color, text, mouse_pos, click):
        super().__init__(x, y, w, h, color, text, mouse_pos, click)
    def display(self, display_surf):
        return super().display(display_surf)
        return self.__click
    def button_func(self):
        vid_path = getVidPath()

        if vid_path == None or vid_path[-3:] not in vid_format:
            showMessage("Error", "We dont support this file")
        else:
            blur_process = threading.Thread(target = blurVid, args=(vid_path, ))
            blur_process.start()

            isCancel = okCancel("Processing", "Please waiting while we blurring your video. \n Click Ok to continue and please wait or \n Click Cancel if you want to cancel this process")

            while blur_process.is_alive():
                if isCancel:
                    gfp.still_blurring = False

            if gfp.still_blurring:
                print("In")
                changeScreen("result")                            

class SaveBtn(Button):
    def __init__(self, x, y, w, h, color, text, mouse_pos, click):
        super().__init__(x, y, w, h, color, text, mouse_pos, click)
    def display(self, display_surf):
        return super().display(display_surf)
    def button_func(self):
        new_path = getSavePath()

        if new_path == "":
            showMessage("Error", "Cant save to that directory")
        else:
            saveVid(new_path)
            showMessage("Saved", "Your video have been saved to " + new_path)
            changeScreen("main")

class CancelBtn(Button):
    def __init__(self, x, y, w, h, color, text, mouse_pos, click):
        super().__init__(x, y, w, h, color, text, mouse_pos, click)
    def display(self, display_surf):
        return super().display(display_surf)
    def button_func(self):
        changeScreen("main")

def okCancel(window_title, message):
    root = Tk()
    root.withdraw()
    cancel = messagebox.askokcancel(window_title, message, parent = root)    

    root.destroy()

    return not cancel

def showMessage(window_title, message):
    root = Tk()
    root.withdraw()
    messagebox.showinfo(window_title, message, parent = root)    

    root.destroy()

def getVidPath():
    root = Tk()
    root.withdraw()

    p = askopenfilename()

    root.destroy()
    
    return p

def getSavePath():
    root = Tk()
    root.withdraw()

    p = asksaveasfilename(title= "Save As", defaultextension= ".mp4", filetypes= [("MP4 video file", ".mp4")])
    print(p)
    root.destroy()

    return p

def changeScreen(next_screen):
    if next_screen == "result":
        result_screen()
    elif next_screen == "main":
        main_menu()

def updateMousepos(btn, mousepos):
    btn.update_mouse_pos(mousepos=mousepos)

def updateClick(btn, click):
    btn.update_click(click=click)

pygame.init()
display_surf = pygame.display.set_mode((612, 480))
pygame.display.set_caption("Menu")

bg_img = pygame.image.load("imgs\mainBG.jpg").convert_alpha()

fps = 60
fps_clock = pygame.time.Clock()

def main_menu():
    deleteVid()

    display_surf.fill((0,0,0))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                flag = True
        
        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        browse_btn = BrowseBtn(206, 419, 200, 50, "white", "BROWSE", mousepos, click)
        screen = Screen([browse_btn], bg_img)

        updateMousepos(browse_btn, mousepos)
        updateClick(browse_btn, click)
        if browse_btn.is_clicked():
            browse_btn.button_func()

        screen.display(display_surf)

        pygame.display.update()
        fps_clock.tick(fps)

def result_screen():
    display_surf.fill((0,0,0))
    pygame.display.flip()

    src = cv2.VideoCapture("output.mp4")
    if src.isOpened() == False:
        print("Noooo")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                flag = True
        
        mousepos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        save_btn = SaveBtn(70, 419, 201, 50, "white", "SAVE", mousepos, click)
        cancel_btn = CancelBtn(341, 419, 201, 50, "red", "CANCEL", mousepos, click)
        btns = [save_btn, cancel_btn]
        screen = Screen(btns)

        for btn in btns:
            updateMousepos(btn, mousepos)
            updateClick(btn, click)
            if btn.is_clicked():
                src.release()
                btn.button_func()

        screen.display(display_surf)

        ret, fr = src.read()

        if ret:
            fr = cv2.resize(fr, (590, 398), interpolation=cv2.INTER_AREA)
            fr = pygame.image.frombuffer(fr.tobytes(), fr.shape[1::-1], "BGR")

            display_surf.blit(fr, (10, 11))
        else:
            src.release()

        pygame.display.update()
        fps_clock.tick(fps)

main_menu()