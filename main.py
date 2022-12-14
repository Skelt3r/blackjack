from components import CardFrame, GameButton
from game import Blackjack
from PIL import Image, ImageTk
from tkinter import Button, Entry, Frame, Label, messagebox, Tk, Toplevel
from time import sleep


class App:
    def __init__(self):
        self.game = Blackjack()
        self.temp_frames = []
        self.temp_labels = []
        self.hit_placer = 0.45

        
    def draw_card_on_screen(self, card, image, pause=True):
        open_image = Image.open(f'./images/{image}.png')
        open_image = open_image.resize((72, 95))
        card.image = ImageTk.PhotoImage(open_image)
        card.configure(image=card.image)
        card.pack()
        if pause: sleep(0.1)
        self.root.update()

    
    def update_banks(self):
        self.game.update_banks()
        self.funds_label['text'] = f'Player funds: ${self.game.player.funds}'
        self.pot_label['text'] = f'Pot: ${self.game.pot}'
    

    def set_bet_amount(self):
        def get_amount():
            try:
                amount = int(entry.get())
                if amount <= 0:
                    messagebox.showerror('Wager not set', 'Wager must be greater than $0.')
                    win.tkraise()
                    entry.focus()
                else:
                    self.wager_label['text'] = f'Wager: ${amount}'
                    win.unbind_all('<Return>')
                    win.unbind_all('<Escape>')
                    win.destroy()
                    return amount
            except ValueError:
                messagebox.showerror('Invalid bet.', 'Enter a valid integer.')

        win = Toplevel(self.root)
        win.title('Set Wager')
        win.attributes('-toolwindow', True)
        win.resizable(0, 0)
        
        label = Label(win, text='Amount:')
        entry = Entry(win, width=10)
        ok = Button(win, text='OK', width=5, command=get_amount)
        cancel = Button(win, text='Cancel', command=win.destroy)

        label.grid(row=0, column=0, sticky='e', padx=5, pady=5)
        entry.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ok.grid(row=1, column=0, sticky='e', padx=5, pady=5)
        cancel.grid(row=1, column=1, padx=5, pady=5)

        win.bind_all('<Return>', lambda _: get_amount())
        win.bind_all('<Escape>', lambda _: win.destroy())
        entry.focus()


    def place_bet(self, amount):
        self.game.player.bet = amount
        self.game.player.funds -= self.game.player.bet
        self.game.pot = self.game.player.bet*2

    
    def clear_board(self):
        for card in self.all_cards: self.draw_card_on_screen(card, 'empty', False)
        for card in self.player_cards: self.draw_card_on_screen(card, 'empty', False)
        for card in self.dealer_cards: self.draw_card_on_screen(card, 'empty', False)
        for frame in self.temp_frames: frame.destroy()
        for label in self.temp_labels: label.destroy()

        self.player_cards = [self.player_card_label1, self.player_card_label2]
        self.dealer_cards = [self.dealer_card_label1, self.dealer_card_label2]
        self.all_cards = [self.player_card_label1, self.player_card_label2, self.dealer_card_label1, self.dealer_card_label2]
        self.player_score_label['text'] = 'Player score: -'
        self.dealer_score_label['text'] = 'Dealer score: -'
        self.deal_button['text'] = 'Deal'
        self.wager_label['text'] = f'Wager: ${self.game.player.bet}'
        self.hit_placer = 0.45
        self.game.stage = 'default'
        self.game.new_round()
        self.configure_buttons()


    def configure_buttons(self):
        match self.game.stage:
            case 'default':
                self.deal_button['text'] = 'Deal'
                self.deal_button.configure(command=self.deal)
                self.bet_button.configure(state='normal')
                self.deal_button.configure(state='normal')
                self.hit_button.configure(state='disabled')
                self.stand_button.configure(state='disabled')
                self.surrender_button.configure(state='disabled')
            case 'player':
                self.bet_button.configure(state='disabled')
                self.deal_button.configure(state='disabled')
                self.hit_button.configure(state='normal')
                self.stand_button.configure(state='normal')
                self.surrender_button.configure(state='normal')
            case 'dealer':
                self.bet_button.configure(state='disabled')
                self.deal_button.configure(state='disabled')
                self.hit_button.configure(state='disabled')
                self.stand_button.configure(state='disabled')
                self.surrender_button.configure(state='disabled')
            case 'next':
                self.deal_button['text'] = 'Next'
                self.deal_button.configure(command=self.clear_board)
                self.bet_button.configure(state='disabled')
                self.deal_button.configure(state='normal')
                self.hit_button.configure(state='disabled')
                self.stand_button.configure(state='disabled')
                self.surrender_button.configure(state='disabled')


    def deal(self):
        self.game.player.bet = int(self.wager_label['text'].split('$')[-1])
        if self.game.player.bet <= 0:
            messagebox.showerror('Wager not set', 'Wager must be greater than $0.')
        else:
            self.place_bet(self.game.player.bet)
            
            for card in self.player_cards:
                self.draw_card_on_screen(card, self.game.player.cards[self.player_cards.index(card)])

            self.draw_card_on_screen(self.dealer_card_label1, self.game.dealer.cards[0])
            
            if self.game.sum_values(self.game.player.cards) == 21:
                self.draw_card_on_screen(self.dealer_card_label2, self.game.dealer.cards[1])
            else:
                self.draw_card_on_screen(self.dealer_card_label2, 'b')

            self.game.player.score = self.game.sum_values(self.game.player.cards)
            self.player_score_label['text'] = f'Player score: {self.game.player.score}'

            if self.game.player.score == self.game.dealer.score == 21:
                self.game.draw = True
                self.game.stage = 'next'
                messagebox.showinfo('Draw', 'The game is a draw.')
            elif self.game.player.score > 21:
                self.game.dealer.won = True
                self.game.stage = 'next'
                messagebox.showinfo('Dealer won', 'Player busted! Dealer won the round!')
            else:
                self.game.stage = 'player'

            self.update_banks()
            self.configure_buttons()

    
    def hit(self):
        self.hit_card_frame = CardFrame(self.background, relx=self.hit_placer, rely=0.6)
        self.hit_card_label = Label(self.hit_card_frame)
        self.hit_placer += 0.025
        
        self.player_cards.append(self.hit_card_label)
        self.temp_frames.append(self.hit_card_frame)
        self.temp_labels.append(self.hit_card_label)

        self.game.deck.draw(self.game.player.cards)
        self.game.player.score = self.game.sum_values(self.game.player.cards)
        self.draw_card_on_screen(self.hit_card_label, self.game.player.cards[self.player_cards.index(self.hit_card_label)])
        self.player_score_label['text'] = f'Player score: {self.game.player.score}'

        if self.game.player.score == 21:
            self.game.stage = 'dealer'
            self.configure_buttons()
            self.dealer_turn()
        elif self.game.player.score > 21:
            self.deal_button['text'] = 'Next'
            self.game.dealer.won = True
            self.game.stage = 'next'
            messagebox.showinfo('Dealer won', 'Player busted! Dealer won the round!')
            self.update_banks()
            self.configure_buttons()


    def stand(self):
        self.game.stage = 'dealer'
        self.configure_buttons()
        self.dealer_turn()

    
    def surrender(self):
        self.game.dealer.won = True
        self.update_banks()
        self.game.new_round()
        self.clear_board()
        self.configure_buttons()

        
    def dealer_turn(self):
        def hit():
            self.hit_card_frame = CardFrame(self.background, relx=self.hit_placer, rely=0.4)
            self.hit_card_label = Label(self.hit_card_frame)
            self.hit_placer += 0.025

            self.dealer_cards.append(self.hit_card_label)
            self.temp_frames.append(self.hit_card_frame)
            self.temp_labels.append(self.hit_card_label)

            self.game.deck.draw(self.game.dealer.cards)
            self.game.dealer.score = self.game.sum_values(self.game.dealer.cards)
            self.draw_card_on_screen(self.hit_card_label, self.game.dealer.cards[self.dealer_cards.index(self.hit_card_label)])
            self.dealer_score_label['text'] = f'Dealer score: {self.game.dealer.score}'

        self.hit_placer = 0.45
        self.draw_card_on_screen(self.dealer_card_label2, self.game.dealer.cards[1])
        self.game.dealer.score = self.game.sum_values(self.game.dealer.cards)

        if self.game.dealer.score == 21:
            self.dealer_score_label['text'] = f'Dealer score: {self.game.dealer.score}'
            self.game.dealer.won = True
        else:
            resolving = True
            while resolving:
                self.dealer_score_label['text'] = f'Dealer score: {self.game.dealer.score}'
                if self.game.dealer.score < self.game.player.score:
                    hit()
                elif self.game.dealer.score == self.game.player.score:
                    if self.game.player.score == 21:
                        self.game.draw = True
                        resolving = False
                    elif self.game.player.score < 21:
                        hit()
                elif self.game.dealer.score > self.game.player.score:
                    if self.game.dealer.score <= 21:
                        self.game.dealer.won = True
                    else:
                        self.game.player.won = True
                    resolving = False

        if self.game.player.funds <= 0:
            messagebox.showinfo('Bankrupt', 'Player went bankrupt! Start a new game.')
            return
        elif self.game.player.won:
            messagebox.showinfo('Player won', 'Player won the round!')
        elif self.game.dealer.won:
            messagebox.showinfo('Dealer won', 'Dealer won the round!')
        else:
            messagebox.showinfo('Draw', 'The game is a draw.')

        self.game.stage = 'next'
        self.update_banks()
        self.configure_buttons()


    def reset(self):
        def ok():
            self.game.__init__()
            self.clear_board()
            self.update_banks()
            self.configure_buttons()
            win.destroy()

        win = Toplevel(self.root)
        win.title('Reset')
        win.attributes('-toolwindow', True)
        win.resizable(0, 0)
        
        Label(win, text='Are you sure you want to reset the board?').grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        Button(win, text='Yes', command=ok, width=5).grid(row=1, column=0, sticky='e', padx=2, pady=5)
        Button(win, text='No', command=win.destroy, width=5).grid(row=1, column=1, sticky='w', padx=2, pady=5)
        
        win.focus()


    def run(self):
        self.root = Tk()
        self.root.geometry('800x600')
        self.root.iconphoto(True, ImageTk.PhotoImage(file='./images/b.png'))
        self.root.title('Blackjack')
        self.root.resizable(0, 0)

        self.background = Frame(self.root, bg='green')
        self.background.place(relwidth=1, relheight=1)

        self.player_card_frame1 = CardFrame(self.background, relx=0.435, rely=0.8)
        self.player_card_frame2 = CardFrame(self.background, relx=0.565, rely=0.8)
        self.dealer_card_frame1 = CardFrame(self.background, relx=0.435, rely=0.2)
        self.dealer_card_frame2 = CardFrame(self.background, relx=0.565, rely=0.2)

        self.player_card_label1 = Label(self.player_card_frame1)
        self.player_card_label2 = Label(self.player_card_frame2)
        self.dealer_card_label1 = Label(self.dealer_card_frame1)
        self.dealer_card_label2 = Label(self.dealer_card_frame2)
        self.funds_label = Label(self.background, text=f'Player funds: ${self.game.player.funds}', font='Terminal', bg='green')
        self.player_score_label = Label(self.background, text='Player score: -', font='Terminal', bg='green')
        self.dealer_score_label = Label(self.background, text='Dealer score: -', font='Terminal', bg='green')
        self.pot_label = Label(self.background, text=f'Pot: ${self.game.pot}', font='Terminal', bg='green')
        self.wager_label = Label(self.background, text=f'Wager: ${self.game.player.bet}', font='Terminal', bg='green')

        self.funds_label.place(relx=0.01, rely=0.01)
        self.player_score_label.place(relx=0.01, rely=0.525)
        self.dealer_score_label.place(relx=0.01, rely=0.475)
        self.pot_label.place(relx=0.825, rely=0.01)
        self.wager_label.place(relx=0.795, rely=0.05)

        self.bet_button = GameButton(self.background, text='Bet', command=self.set_bet_amount, relx=0.825, rely=0.1)
        self.deal_button = GameButton(self.background, text="Deal", command=self.deal, relx=0.875, rely=0.425)
        self.reset_button = GameButton(self.background, text="Reset", command=self.reset, relx=0.875, rely=0.525)
        self.hit_button = GameButton(self.background, text="Hit", command=self.hit, relx=0.3, rely=0.915, state='disabled')
        self.stand_button = GameButton(self.background, text="Stand", command=self.stand, relx=0.425, rely=0.915, state='disabled')
        self.surrender_button = GameButton(self.background, text="Surrender", command=self.surrender, relx=0.55, rely=0.915, relwidth=0.155, state='disabled')

        self.all_cards = [self.player_card_label1, self.player_card_label2, self.dealer_card_label1, self.dealer_card_label2]
        self.player_cards = [self.player_card_label1, self.player_card_label2]
        self.dealer_cards = [self.dealer_card_label1, self.dealer_card_label2]

        self.root.mainloop()


if __name__ == '__main__':
    app = App()
    app.run()
