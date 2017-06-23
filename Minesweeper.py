# Python Version 3.6

import tkinter
from tkinter import messagebox
import random
import time
import math


class Minesweeper():
    def __init__(self, master, retry_diffic):
        # set up frame
        self.frame = tkinter.Frame(master)
        self.info_frame = tkinter.Frame(master) # show the number of mine, clicked, time, retry btn
        self.init_frame = tkinter.Frame(master) # choose difficulty
        self.init_frame.pack(padx=10, pady=10)

        # initialization
        self.start_time = time.time()
        self.running_time = tkinter.IntVar(value=0)

        self.first_try = 1 # 1 : Preventing First Click from being Mine
        self.max=0
        self.flag = 0
        self.mines = tkinter.IntVar(value=0) # the number of mine
        self.clicked_num = tkinter.IntVar(value=0) # the number of clicked
        self.Diffic_Var = tkinter.StringVar(value='0')
        self.prob = 0

        # import images
        self.watch = tkinter.PhotoImage(file="images/watch.png")
        self.tile_plain = tkinter.PhotoImage(file="images/tile_plain.gif")
        self.tile_clicked = tkinter.PhotoImage(file="images/tile_clicked.gif")
        self.tile_mine = tkinter.PhotoImage(file="images/tile_mine.gif")
        self.tile_flag = tkinter.PhotoImage(file="images/tile_flag.gif")
        self.tile_wrong = tkinter.PhotoImage(file="images/tile_wrong.gif")
        self.tile_no = []
        for x in range(1, 9):
            self.tile_no.append(tkinter.PhotoImage(file="images/tile_" + str(x) + ".gif"))

        # Game Start
        self.set_menubar(master)
        if retry_diffic == '0':
            self.choose_difficulty()
        else:
            self.Diffic_Var.set(retry_diffic)
            self.clear_init_frame()
        self.grid_widgets()

    # END OF __init__

    def set_menubar(self, master):
        menubar = tkinter.Menu(master)
        master['menu'] = menubar

        game_menu = tkinter.Menu(menubar, tearoff=0, bd=5)
        menubar.add_cascade(label="Game", menu=game_menu)
        setting_menu = tkinter.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Setting", menu=setting_menu)

        game_menu.add_command(label="New Game", command=self.Retry)
        game_menu.add_separator()
        game_menu.add_command(label="Exit", command=master.destroy)
        setting_menu.add_command(label="There's no setting yet.")

    def choose_difficulty(self):
        self.Diffic_Var.set(0)
        self.Difficulty_low = tkinter.Radiobutton(self.init_frame, text="Easy mode           ", variable = self.Diffic_Var, value="Easy")
        self.Difficulty_mid = tkinter.Radiobutton(self.init_frame, text="Intermediate mode", variable = self.Diffic_Var, value="Intermediate")
        self.Difficulty_high = tkinter.Radiobutton(self.init_frame, text="Hard mode           ", variable = self.Diffic_Var, value="Hard")
        self.Difficulty_low.grid(row=1, column=0, padx=20, pady=5)
        self.Difficulty_mid.grid(row=2, column=0, padx=20, pady=5)
        self.Difficulty_high.grid(row=3, column=0, padx=20, pady=5)
        self.Start_btn = tkinter.Button(self.init_frame, padx=5, pady=5, text="Start", command=self.clear_init_frame)
        self.Start_btn.grid(row=2, column=1, padx=10, rowspan=1)

    def clear_init_frame(self):
        self.init_frame.destroy() # destroy Choosing Diffic window

        # set diff
        if self.Diffic_Var.get() == "Easy":
            self.prob = 0.16
            self.max = 5
        elif self.Diffic_Var.get() == "Intermediate":
            self.prob = 0.20
            self.max = 10
        elif self.Diffic_Var.get() == "Hard":
            self.prob = 0.25
            self.max = 20
        else:
            tkinter.messagebox.showerror("Initialization Fail..", "Choose Difficulty.")
            root.destroy()
            main()
        # set up new frame
        self.frame.pack(padx=20, pady=10)
        self.info_frame.pack()
        self.create_buttons()
        # set up timer
        self.timer()

    def timer(self):
        temp = math.floor(time.time()-self.start_time)
        self.running_time.set(temp)
        self.info_frame.after(500, self.timer)

    def create_buttons(self):
        # create buttons
        self.buttons = dict({})
        while True:
            x_coord = 0
            y_coord = 1
            for x in range(0, self.max ** 2):
                mine = 0
                if random.uniform(0.0, 1.0) < self.prob:  # prob = 0.13 or 0.20 or 0,25
                    mine = 1
                    self.mines.set(self.mines.get() + 1)
                # 0 = Button widget
                # 1 = if a mine y/n (1/0)
                # 2 = state (0 = unclicked, 1 = clicked, 2 = flagged)
                # 3 = button id
                # 4 = [x, y] coordinates in the grid
                self.buttons[x] = [tkinter.Button(self.frame, image=self.tile_plain), mine, 0, x, [x_coord, y_coord]]
                self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
                self.buttons[x][0].bind('<Button-3>', self.rclicked_wrapper(x))

                # calculate coords:
                x_coord += 1
                if x_coord == self.max:
                    x_coord = 0
                    y_coord += 1

            if self.mines.get() == 0:
                continue
            else:
                break

        # lay buttons in grid
        for key in self.buttons:
            self.buttons[key][0].grid(row=self.buttons[key][4][1], column=self.buttons[key][4][0])

    def grid_widgets(self):
        # show Title at the top
        self.Main_Label = tkinter.Label(self.frame, text="Minesweeper")
        self.Main_Label.grid(row=0, column=0, columnspan=30)
        # lay information in grid
        self.lb_mine = tkinter.Label(self.info_frame, text="Mine :")
        self.lb_mine.grid(row=self.max + 2, column=0)
        self.lb_mine_num = tkinter.Label(self.info_frame, textvariable=self.mines)
        self.lb_mine_num.grid(row=self.max + 2, column=1)
        self.lb_clicked = tkinter.Label(self.info_frame, text="Click :")
        self.lb_clicked.grid(row=self.max + 2, column=3, sticky='e')
        self.lb_clicked_num = tkinter.Label(self.info_frame, textvariable=self.clicked_num)
        self.lb_clicked_num.grid(row=self.max + 2, column=4)
        self.image_time = tkinter.Button(self.info_frame, image=self.watch, borderwidth=0)
        self.image_time.grid(row=self.max + 3, column=0)
        self.lb_time = tkinter.Label(self.info_frame, textvariable=self.running_time)
        self.lb_time.grid(row=self.max + 3, column=1)
        self.retry = tkinter.Button(self.info_frame, text="Retry", command=self.Retry, padx=1)
        self.retry.grid(row=self.max + 3, column=3, padx=10, columnspan=3, sticky='we')
        self.empty_lb = tkinter.Label(self.info_frame, text="   ")
        self.empty_lb.grid(row=self.max + 2, column=2)

    def lclicked_wrapper(self, x):
        return lambda Button: self.lclicked(x)

    def rclicked_wrapper(self, x):
        return lambda Button: self.rclicked(x)

    def make_one_mine(self):
        while True:
            temp_x = random.randrange(0, self.max)
            if self.buttons[temp_x][1] == 1: # if mine
                continue
            elif self.buttons[temp_x][1] == 0: #if not mine
                self.buttons[temp_x][1] = 1 # make this mine
                break
        self.first_try = 0

    def lclicked(self, x):
        # if found Mine in the first attempt.
        if self.first_try == 1 and self.buttons[x][1] == 1:
            self.buttons[x][1] = 0
            self.make_one_mine()
        else:
            self.first_try=0

        # if mine
        if self.buttons[x][1] == 1:
            self.show_all_mines_lose()
            self.gameover()
        # if not mine
        else:
            self.clicked_num.set(self.clicked_num.get()+1)
            self.buttons[x][2] = 1

            self.check_nearby(x)
            self.buttons[x][0].unbind('<Button-1>')
            if self.mines.get()+self.clicked_num.get()+self.flag == self.max**2:
                self.show_all_mines_win()
                self.victory()

    def rclicked(self, x):
        # if not flaged
        if self.buttons[x][2] == 0:
            self.buttons[x][0].config(image=self.tile_flag)
            self.buttons[x][2] = 2
            self.buttons[x][0].unbind('<Button-1>')
            self.mines.set(self.mines.get() - 1)
            self.flag += 1
        # if flaged already
        elif self.buttons[x][2] == 2:
            self.buttons[x][2] = 0
            self.buttons[x][0].config(image=self.tile_plain)
            self.buttons[x][0].bind('<Button-1>', self.lclicked_wrapper(x))
            self.mines.set(self.mines.get() + 1)
            self.flag -= 1

    def show_all_mines_lose(self):
        # show all mines
        for x in self.buttons:
            if self.buttons[x][1] == 1:  # if mine
                self.buttons[x][0].config(image=self.tile_wrong)

    def show_all_mines_win(self):
        # show all mines
        for x in self.buttons:
            if self.buttons[x][1] == 1:  # if mine
                self.buttons[x][0].config(image=self.tile_mine)

    def check_nearby(self, x):
        idx = x
        count = 0
        for i in [0,1,1]:
            idx += i*self.max
            for j in range(-1, 2):
                key = idx- self.max + j

                if key<0 or key>=self.max**2: # none exist space
                    continue
                elif idx % self.max == self.max - 1 and key%self.max ==0 : # physically not close space
                    continue
                elif idx % self.max == 0 and key % self.max == self.max - 1: # physically not close space
                    continue
                elif self.buttons[key][1] == 1: # if mine
                    count+=1

        self.change_to_tile_no(x, count)

    def show_nearby_none_mine(self, x):
        idx = x
        for i in [0, 1, 1]:
            idx += i * self.max
            for j in range(-1, 2):
                key = idx - self.max + j

                if key < 0 or key >= self.max ** 2:  # none exist space
                    continue
                elif idx % self.max == self.max - 1 and key % self.max == 0:  # physically not close space
                    continue
                elif idx % self.max == 0 and key % self.max == self.max - 1:  # physically not close space
                    continue
                elif self.buttons[key][1] == 0 and self.buttons[key][2] != 1:  # if not mine and unclicked
                    self.lclicked(key)

    def change_to_tile_no(self, x, count):
        if count != 0:
            self.buttons[x][0].config(image=self.tile_no[count-1])

        elif count == 0:
            self.buttons[x][0].config(image=self.tile_clicked)
            self.show_nearby_none_mine(x)

    def gameover(self):
        ask_retry = tkinter.messagebox.askokcancel("You Lose.", "Try again?")
        if ask_retry == True:
            self.Retry()
        else:
            root.destroy()

    def victory(self):
        ask_retry = tkinter.messagebox.askokcancel("You Win.", "Congratulation.\nWould you like to Try again?")
        if ask_retry == True:
            self.Retry()
        else:
            root.destroy()

    def Retry(self):
        root.destroy()
        main(self.Diffic_Var.get())

# END OF minesweeper (class)


def main(retry_diffic='0'):
    global root
    root = tkinter.Tk()
    root.title("Minesweeper")
    game = Minesweeper(root, retry_diffic)
    root.mainloop()

if __name__ == "__main__":
    main()


