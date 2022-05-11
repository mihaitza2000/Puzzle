import pygame, cv2, os, shutil, random, ctypes, PIL.Image
from pygame import *
import numpy as np
from time import sleep
from tkinter import *
from os import listdir
from os.path import isfile, join
from PIL import ImageTk, Image

width, height, moves, num, cuts, speed = 500, 500, -1, False, -1, 0.1
root_path = "./images"
onlyfiles = [f for f in listdir(root_path) if isfile(join(root_path, f))]
selected = False
side = width//cuts
user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
w, h, w3, h3 = 500, 500, 500, 300
posX3, posY3 = screensize[0]//2-w3//2, screensize[1]//2 - h3//2
w2, h2 = w, 3*h//4
pictures, Pieces, L, index = [], [], [], 0
posX, posY = screensize[0]//2-w//2, screensize[1]//2 - h//2
posX2, posY2 = screensize[0]//2-w2//2, screensize[1]//2 - h2//2
image_selected = f"{root_path}/image1.jpg"
continue_var = True

def submit_button(win):
    if cuts > 0 and moves > 0:
        win.destroy()

def button_config(b1, b2, b3, type_button):
    global cuts, moves, side
    b1.config(bg = "red")
    if type_button == "cut":
        cuts = int(b1["text"])
        side = width // cuts
    else:
        moves = int(b1["text"])
    b2.config(bg = "green")
    b3.config(bg = "green")

def select_level(win):
    
    img3 = Image.open("./images/level/up.png")
    resized3 = img3.resize((w2, h2//2))
    image3 = ImageTk.PhotoImage(resized3)
    label_up = Label(win, image = image3)
    label_up.place(x = 0, y = 0)
    
    img4 = Image.open("./images/level/down.png")
    resized4 = img4.resize((w2, h2//2))
    image4 = ImageTk.PhotoImage(resized4)
    label_down = Label(win, image = image4)
    label_down.place(x = 0, y = h2//2)
    
    label1 = Label(win, text = "Number of cuts: ", font = ("", 16))
    label1.place(x = w2//4, y = h2//4, anchor = "center")
    
    label2 = Label(win, text = "Number of moves: ", font = ("", 16))
    label2.place(x = w2//4, y = 3*h2//4, anchor = "center")
    
    b1_cuts = Button(win, text = "2", width = w2//100, bg = "green")
    b1_cuts.place(x = w2//2 + w2//12, y = h2//4, anchor = "center")
    
    b2_cuts = Button(win, text = "5", width = w2//100, bg = "green")
    b2_cuts.place(x = w2//2 + 3*w2//12, y = h2//4, anchor = "center")
    
    b3_cuts = Button(win, text = "10", width = w2//100, bg = "green")
    b3_cuts.place(x = w2//2 + 5*w2/12, y = h2//4, anchor = "center")
    
    b1_moves = Button(win, text = "10", width = w2//100, bg = "green")
    b1_moves.place(x = w2//2 + w2//12, y = 3*h2//4, anchor = "center")
    
    b2_moves = Button(win, text = "50", width = w2//100, bg = "green")
    b2_moves.place(x = w2//2 + 3*w2//12, y = 3*h2//4, anchor = "center")
    
    b3_moves = Button(win, text = "100", width = w2//100, bg = "green")
    b3_moves.place(x = w2//2 + 5*w2/12, y = 3*h2//4, anchor = "center")
    
    b1_cuts.config(command = lambda: button_config(b1_cuts, b2_cuts, b3_cuts, "cut"))
    b2_cuts.config(command = lambda: button_config(b2_cuts, b1_cuts, b3_cuts, "cut"))
    b3_cuts.config(command = lambda: button_config(b3_cuts, b1_cuts, b2_cuts, "cut"))
    
    b1_moves.config(command = lambda: button_config(b1_moves, b2_moves, b3_moves, "move"))
    b2_moves.config(command = lambda: button_config(b2_moves, b1_moves, b3_moves, "move"))
    b3_moves.config(command = lambda: button_config(b3_moves, b1_moves, b2_moves, "move"))
    
    submit_moves = Button(win, text = "Submit", width = w2//80, bg = "red", command = lambda: submit_button(win))
    submit_moves.place(x = w2//2, y = h2//2, anchor = "center")
    
    win.mainloop()

def mix(list):
    global L
    [x, y] = list[random.randint(0, len(list)-1)]
    L.append([[x,y],get_empty()])
    swap([x,y],get_empty())

def get_full():
    [x, y] = get_empty()
    list = []
    if x < cuts-1:
        list.append([x+1, y])
    if y < cuts-1:
        list.append([x, y+1])
    if x > 0:
        list.append([x-1, y])
    if y > 0:
        list.append([x, y-1])
    return list

def get_empty():
    for i in range(cuts):
        for j in range(cuts):
            if Pieces[i][j].empty:
                return [i,j]

def delete(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))   

def slicer(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (width, height), interpolation = cv2.INTER_AREA)
    for i in range(cuts):
        for j in range(cuts):
            cv2.imwrite(f'./pieces/pic_{i*cuts+j}.jpg', img[i*side:(i+1)*side,j*side:(j+1)*side])

def swap(new, old):
    aux = Pieces[new[0]][new[1]].img
    Pieces[new[0]][new[1]].img = Pieces[old[0]][old[1]].img
    Pieces[old[0]][old[1]].img = aux
    
    aux = Pieces[new[0]][new[1]].empty
    Pieces[new[0]][new[1]].empty = Pieces[old[0]][old[1]].empty
    Pieces[old[0]][old[1]].empty = aux
    
    aux = Pieces[new[0]][new[1]].text
    Pieces[new[0]][new[1]].text = Pieces[old[0]][old[1]].text
    Pieces[old[0]][old[1]].text = aux
    Pieces[old[0]][old[1]].text = aux
    
    aux = Pieces[new[0]][new[1]].number
    Pieces[new[0]][new[1]].number = Pieces[old[0]][old[1]].number
    Pieces[old[0]][old[1]].number = aux
    Pieces[old[0]][old[1]].number = aux

def test(x, y):
    if x < cuts-1 and Pieces[x+1][y].empty:
        return [x+1, y]
    elif y < cuts-1 and Pieces[x][y+1].empty:
        return [x, y+1]
    elif x > 0 and Pieces[x-1][y].empty:
        return [x-1, y]
    elif y > 0 and Pieces[x][y-1].empty:
        return [x, y-1]
    else:
        return []

def init_images():
    for i in range(cuts):
        list = []
        for j in range(cuts):
            path = f'./pieces/pic_{i*cuts+j}.jpg'
            picture = pygame.image.load(path)
            picture = pygame.transform.scale(picture,(side, side))
            list.append(picture)
        pictures.append(list)
    nr = 1
    for i in range(cuts):
        list = []
        for j in range(cuts):
            p = Piece(i, j, pictures[j][i], nr)
            nr += 1
            list.append(p)
        Pieces.append(list)
    delete('./pieces')
    
def show():
    global Pieces, rectPosX, rectPosY, pick
    screen.fill((0,0,0)) 
    for i in range(cuts):
        for j in range(cuts):
            Pieces[i][j].show()
            if Pieces[i][j].empty:
                rect = pygame.Surface((side, side))
                rect.fill((0,0,0))
                screen.blit(rect,(i*side, j*side))
    for i in range(cuts-1):
        pygame.draw.line(screen, (0,0,255), ((i+1)*side, 0), ((i+1)*side, height))
        pygame.draw.line(screen, (0,0,255), (0, (i+1)*side), (width, (i+1)*side))

def close_win(win):
    global selected
    selected = True
    win.destroy()

def init(win):
    global root_path, onlyfiles
    index = 0
    
    img = Image.open(f"{root_path}/{onlyfiles[index]}")
    resized = img.resize((w, h))
    image_bg = ImageTk.PhotoImage(resized)
    label = Label(win, image = image_bg)
    label.pack()
    
    img1 = Image.open(f"{root_path}/arrows/left_arrow.png")
    resized1 = img1.resize((w//8, h//8))
    image1 = ImageTk.PhotoImage(resized1)
    left_arrow_button = Button(win, image = image1, command = lambda: slide_left(label))
    left_arrow_button.place(x = w//16, y = h//2, anchor = "center")
    
    img2 = Image.open(f"{root_path}/arrows/right_arrow.png")
    resized2 = img2.resize((w//8, h//8))
    image2 = ImageTk.PhotoImage(resized2)
    right_arrow_button = Button(win, image = image2,command = lambda: slide_right(label))
    right_arrow_button.place(x = w-w//16, y = h//2, anchor = "center")
    
    img3 = Image.open(f"{root_path}/arrows/button.png")
    resized3 = img3.resize((w//4, h//8))
    image3 = ImageTk.PhotoImage(resized3)
    press_button = Button(win, image = image3, command = lambda: close_win(win))
    press_button.place(x = w/2, y = h-h//10, anchor = "center")
    
    win.mainloop()

def slide_left(label):
    global index
    if index > 0:
        index -= 1
    img = Image.open(f"{root_path}/{onlyfiles[index]}")
    resized = img.resize((w, h))
    image = ImageTk.PhotoImage(resized, Image.ANTIALIAS)
    label.configure(image = image)
    label.image = image

def slide_right(label):
    global index
    if index < 2:
        index += 1
    img = Image.open(f"{root_path}/{onlyfiles[index]}")
    resized = img.resize((w, h))
    image = ImageTk.PhotoImage(resized, Image.ANTIALIAS)
    label.configure(image = image)
    label.image = image

class Piece:
    def __init__(self, x, y, img, nr):
        self.x = x
        self.y = y
        self.img = img
        self.text = myfont.render(f'{y*cuts+x+1}',False, (0, 0, 0))
        self.number = nr
        if x == cuts-1 and y == cuts-1:
            self.empty = True
        else:
            self.empty = False
    def show(self):
        screen.blit(self.img, (self.x*side, self.y*side))
        if num:
            screen.blit(self.text,(self.x*side+side//3, self.y*side+side//6))
            
    def test(self):
        if self.number == self.x*cuts+self.y+1:
            return True

def continue_funtion(win, answer):
    global continue_var
    if answer == "yes": 
        continue_var = True
    else:
        continue_var = False
    win.destroy()

def selection_function(win):
    img_wallpaper = Image.open("./images/buttons/bg.jpg")
    resized_wallpaper = img_wallpaper.resize((w3, h3))
    image_wallpaper = ImageTk.PhotoImage(resized_wallpaper)
    label1 = Label(win, image = image_wallpaper).pack()
    label2 = Label(win, text = "Do you want to continue ?", font = ("", 30))
    label2.place(x = w3//2, y = h3//4, anchor = "center")
    
    img_yes = Image.open("./images/buttons/yes.jpg")
    resized_yes = img_yes.resize((w3//2, h3//2))
    image_yes = ImageTk.PhotoImage(resized_yes)
    yes_button = Button(win, image = image_yes, width = w3//2, command = lambda: continue_funtion(win, "yes"))
    yes_button.place(x = 0, y = h3//2)
    
    img_no = Image.open("./images/buttons/no.jpg")
    resized_no = img_no.resize((w3//2, h3//2))
    image_no = ImageTk.PhotoImage(resized_no)
    no_button = Button(win, image = image_no, width = w3//2, command = lambda: continue_funtion(win, "no"))
    no_button.place(x = w3//2, y = h3//2)
    
    win.mainloop()

if __name__ == "__main__": 

    while continue_var:
        win = Tk()
        win.geometry(f"{w3}x{h3}+{posX3}+{posY3}")
        selection_function(win)
        if continue_var:
            win = Tk()
            win.geometry(f"{w}x{h}+{posX}+{posY}")
            init(win)
            
            win = Tk()
            win.geometry(f"{w2}x{h2}+{posX2}+{posY2}")
            select_level(win)
            
            if selected:
                pygame.init()
                screen = pygame.display.set_mode([width, height])
                myfont = pygame.font.SysFont('Calibri', side//4)
                slicer(f"{root_path}/{onlyfiles[index]}")
                init_images()
                mix(get_full())
                done = True
                while done:
                    mouse = pygame.mouse.get_pos()
                    pygame.display.flip()
                    if moves > 0:
                        sleep(speed)
                        list = get_full()
                        mix(list)
                        moves -= 1
                    for event in pygame.event.get():
                        if event.type == QUIT:
                            quit() 
                        elif event.type == pygame.MOUSEBUTTONDOWN:
                            if not test(mouse[0]//side, mouse[1]//side) == []:
                                swap(test(mouse[0]//side, mouse[1]//side), [mouse[0]//side, mouse[1]//side])
                        elif event.type == KEYDOWN:
                            if event.key == K_n:
                                if num:
                                    num = False
                                else:
                                    num = True
                    if moves == 0:
                        l = []
                        for i in range(cuts):
                            for j in range(cuts):
                                l.append(Pieces[i][j].number)
                        if l == [i  for i in range(1,cuts*cuts+1)]:
                            done = False
                    show()
                pygame.display.flip()
                show()
                sleep(3)
                pygame.quit()
                selected = False
    
    
    
    
    