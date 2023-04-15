from tkinter import *
from tkinter import messagebox
from tkinter import ttk

from findWordcls import FindWords


class FindWordsGUI(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.puzzle = FindWords(16, 'medium', 'random')
        self.pzl = []
        self.sol = {}
        self.start = 0
        self.wordPos = []

        self.geometry('1300x715')
        self.title("Find Word game")
        self.resizable(0, 0)

        img_bg = PhotoImage(file='imgs\\bg.png')
        Label(self, image=img_bg).place(x=-2, y=0)

        self.btns = [[Button(self, text=' ') for _ in range(16)]
                     for _ in range(10)]

        self.putPuzzle()
        self.genrateFlag = 0
        ############
        with open('txtFiles\\totalwordsfound.txt', 'r') as f:
            self.totalWordsFound = ttk.Label(self, text=f.read(),
                                             font=('', 20, ''), background='#F5F5F5')
        self.totalWordsFound.place(x=300, y=73)
        ############

        ############
        self.timer = ttk.Label(self, text='0s', font=(
            '', 18, ''), background="#bee3f8")
        self.timer.place(x=285, y=173)

        self.from_ = ttk.Label(self, text='',font=('', 15, ''),
                               width=17, background='#fff')
        self.from_.place(x=130, y=232)

        self.to = ttk.Label(self, text='', font=('', 15, ''),
                            width=17, background='#fff')
        self.to.place(x=130, y=278)

        self.foundWords = ttk.Label(
            self, text='0', font=('', 18, ''), background="#bee3f8")
        self.foundWords.place(x=200, y=322)
        ############

        ############
        self.wordKind = ttk.Combobox(self, width=13, values=['random', 'sports', 'programming', 'business'],
                                     font=('', 14, ''), state='readonly')
        self.wordKind.place(x=56, y=360)
        self.wordKind.current(0)

        self.hardKind = ttk.Combobox(self, width=9, values=['easy', 'medium', 'hard'],
                                     font=('', 14, ''), state='readonly')
        self.hardKind.place(x=232, y=360)
        self.hardKind.current(1)
        ############

        ############
        self.img_find = PhotoImage(file='imgs\\find.png')
        self.img_nowords = PhotoImage(file='imgs\\nowords.png')
        self.img_generate = PhotoImage(file='imgs\\genrate.png')

        ttk.Button(image=self.img_find, padding=-1,
                   command=self.find).place(x=56, y=395)

        ttk.Button(image=self.img_nowords, padding=-1,
                   command=self.complete).place(x=164, y=395)

        ttk.Button(image=self.img_generate, padding=-1,
                   command=self.generatePazel).place(x=56, y=409 + 25)
        ############

        self.protocol("WM_DELETE_WINDOW",self.saveFilesAndClose)
        try:
            from ctypes import windll
            windll.shcore.SetProcessDpiAwareness(1)
        finally:
            self.mainloop()

    def complete(self):
        if not self.sol and self.genrateFlag:
            self.genrateFlag = 0
            messagebox.showinfo('nice',f'good job. the puzzle complete in {self.timer["text"]}.'
                                       f' generate another one to play.')
            self.timer['text'] = '0s'

        else:
            messagebox.showwarning('wait','some words still there, or you did not generate a puzzle.')

    def saveFilesAndClose(self):
        with open('txtFiles\\totalwordsfound.txt', 'w') as f:
            f.write(self.totalWordsFound['text'])

        self.destroy()

    def putPosition(self, pos):
        if not self.genrateFlag:
            messagebox.showerror('error', 'sorry you must genrate puzzle.')
            return

        if not self.wordPos:
            self.from_['text'] = f'{int(pos[0])+1}, {int(pos[1])+1}'
            self.wordPos.append(pos)

        elif len(self.wordPos) == 1:
            self.to['text'] = f'{int(pos[0])+1}, {int(pos[1])+1}'
            self.wordPos.append(pos)

        elif len(self.wordPos) == 2:
            self.from_['text'] = f'{int(pos[0])+1}, {int(pos[1])+1}'
            self.to['text'] = ''
            self.wordPos = [pos]

    def find(self):
        if len(self.wordPos) != 2:
            messagebox.showerror('error', 'there is some filed/s empty')
            return

        answer = self.puzzle.checkAnswer(self.wordPos)
        if answer[0]:
            self.foundWords['text'] = str(int(self.foundWords['text']) + 1)
            self.from_['text'] = ''
            self.to['text'] = ''

            for r in range(int(self.wordPos[0][1]), int(self.wordPos[1][1]) + 1):
                for c in range(int(self.wordPos[0][0]), int(self.wordPos[1][0]) + 1):
                    self.btns[r][c]['text'] = '-'

            self.wordPos = []
            del self.sol[answer[1]]

            self.totalWordsFound['text'] = str(int(self.totalWordsFound['text'])+1)

    def putPuzzle(self):
        xp = 420
        yp = 175
        for r in range(10):
            ttk.Label(self, text=str(r + 1), font=('', 15, ''), background='#bee3f8').place(x=390, y=yp + 5)

            for c in range(16):
                self.btns[r][c] = Button(self, text=" ", width=3, font=('', 15, ''), relief='flat',
                                         bg='#fff', command=lambda pos=(str(c), str(r)): self.putPosition(pos))

                self.btns[r][c].place(x=xp, y=yp)
                ttk.Label(self, text=str(c + 1), font=('', 15, ''), background='#bee3f8').place(x=xp + 5, y=145)

                xp += 51
            yp += 50
            xp = 420

    def addTime(self):
        self.timer['text'] = str(int(self.timer['text'][:-1]) + 1) + 's'
        if self.genrateFlag:
            self.timer.after(1000, self.addTime)

    def generatePazel(self):
        self.genrateFlag = 1

        self.puzzle = FindWords(16, self.hardKind.get(), self.wordKind.get())
        self.pzl = self.puzzle.puzzle
        self.sol = self.puzzle.sol

        self.timer['text'] = '0s'
        self.foundWords['text'] = '0'

        if not self.start:
            self.addTime()
            self.start = 1

        for r in range(10):
            for c in range(16):
                self.btns[r][c]['text'] = self.pzl[r][c]


FindWordsGUI()
# NOTE: this code made by Ibrahim Awny.
