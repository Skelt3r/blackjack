from random import shuffle as r_shuffle
from tkinter import Button, Frame


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __repr__(self):
        match self.suit:
            case 1: suit = 'c'  # Cloves
            case 2: suit = 'd'  # Diamonds
            case 3: suit = 'h'  # Hearts
            case 4: suit = 's'  # Spades
        
        return f'{self.value}{suit}'


class Deck(list):
    def __init__(self):
        super().__init__()
        suits = list(range(1, 5))
        values = list(range(1, 14))
        [[self.append(Card(s, v)) for s in suits] for v in values]

    def shuffle(self):
        r_shuffle(self)

    def draw(self, location):
        location.append(self.pop(0))


class Player:
    def __init__(self):
        self.cards = list()
        self.funds = 1000
        self.bet = 0
        self.score = 0
        self.won = False


class CardFrame(Frame):
    def __init__(self, master=None, bg='green', bd='2', relief='solid', relx=1, rely=1, width=75, height=99, anchor='c'):
        super().__init__(master=master, bg=bg, bd=bd, relief=relief)
        self.place(relx=relx, rely=rely, width=width, height=height, anchor=anchor)


class GameButton(Button):
    def __init__(self, master=None, state='normal', text='', font='Terminal', bg='black', fg='orange', bd=5, relief='ridge',
                 activebackground='orange', activeforeground='black', command=None, relx=0, rely=0, relwidth=0.1):
        super().__init__(master=master, state=state, text=text, font=font, bg=bg, fg=fg, bd=bd, relief=relief,
                         activebackground=activebackground, activeforeground=activeforeground,command=command)
        self.place(relx=relx, rely=rely, relwidth=relwidth)
