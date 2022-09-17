from components import Deck, Player
from rich.console import Console


class Blackjack:
    def __init__(self):
        self.console = Console()
        self.deck = Deck()
        self.player = Player()
        self.dealer = Player()
        self.pot = 0
        self.stage = 'default'
        self.draw = False
        
        self.deck.shuffle()

        for _ in range(2): self.deck.draw(self.player.cards)
        for _ in range(2): self.deck.draw(self.dealer.cards)

        self.player.score = self.sum_values(self.player.cards)
        self.dealer.score = self.sum_values(self.dealer.cards)

    
    def new_round(self):
        self.deck = Deck()
        self.stage = 'default'
        self.player.bet = 0
        self.player.won = False
        self.dealer.won = False
        self.draw = False

        self.player.cards.clear()
        self.dealer.cards.clear()
        self.deck.shuffle()

        for _ in range(2): self.deck.draw(self.player.cards)
        for _ in range(2): self.deck.draw(self.dealer.cards)

        self.player.score = self.sum_values(self.player.cards)
        self.dealer.score = self.sum_values(self.dealer.cards)


    def update_banks(self):
        if self.player.won:
            self.player.funds += self.pot
        elif self.draw:
            self.player.funds += int(self.pot//2)

        if self.stage == 'next':
            self.pot = 0

    
    def sum_values(self, location):
        values = [int(str(card)[:-1]) for card in location]

        for i in range(len(values)):
            if values[i] > 10:
                values[i] = 10
            elif values[i] == 1:
                if not (sum(values)+10) > 21:
                    values[i] = 11
        
        return sum(values)

    
    def place_bets(self):
        self.player.funds -= self.player.bet
        self.pot = self.player.bet*2


    def get_player_input(self):
        i = input('What would you like to do?\n>>> ').lower()
        match i:
            case 'hit':
                self.hit()
            case 'stand':
                self.stand()
            case 'surrender':
                self.surrender()
            case 'exit' | 'quit':
                exit('\nExiting game...\n')
            case _:
                self.console.print('\nInvalid input. You must hit, stand, or surrender.\n', style='red')
                self.get_player_input()
        
        self.evaluate_score(self.stage)

    
    def evaluate_score(self, stage):
        if stage == 'player':
            if self.player.score > 21:
                self.dealer.won = True
                self.stage == 'next'
                self.declare_winner()
                self.update_banks()
                self.new_round()
            elif self.player.score == 21:
                self.stage = 'dealer'
                self.print_player_hand()
                self.resolve()
            else:
                self.print_player_hand()
                self.get_player_input()
        elif stage == 'dealer':
            if self.dealer.score > 21:
                self.player.won = True
                self.stage = 'next'
                self.declare_winner()
                self.update_banks()
                self.new_round()
            elif self.dealer.score == 21:
                if self.dealer.score > self.player.score:
                    self.dealer.won = True
                    self.stage = 'next'
                    self.declare_winner()
                    self.update_banks()
                    self.new_round()
                else:
                    self.draw = True
                    self.stage = 'next'
                    self.declare_winner()
                    self.update_banks()
                    self.new_round()
            elif self.dealer.score < 21:
                if self.dealer.score > self.player.score:
                    self.dealer.won = True
                    self.stage = 'next'
                    self.declare_winner()
                    self.update_banks()
                    self.new_round()
                elif self.dealer.score <= self.player.score:
                    self.resolve()

    
    def hit(self):
        self.stage = 'player'
        self.deck.draw(self.player.cards)
        self.player.score = self.sum_values(self.player.cards)
        self.evaluate_score(self.stage)


    def stand(self):
        self.stage = 'dealer'
        self.evaluate_score(self.stage)


    def surrender(self):
        self.console.print('\nPlayer surrendered. Dealer wins the round.')
        self.dealer.won = True
        self.update_banks()
        self.new_round()


    def resolve(self):
        self.player.score = self.sum_values(self.player.cards)
        if (self.dealer.score > self.player.score or
            self.dealer.score == self.player.score == 21 or
            self.dealer.score > 21):
            self.evaluate_score('dealer')
        elif (self.dealer.score < self.player.score or
            (self.dealer.score == self.player.score < 21)):
            self.deck.draw(self.dealer.cards)
            self.dealer.score = self.sum_values(self.dealer.cards)
            self.evaluate_score('dealer')


    def declare_winner(self):
        self.print_player_hand()
        self.print_dealer_hand()
        if self.player.funds > 0 or self.player.won:
            if self.player.won:
                self.console.print('Player won the round', style='green')
            elif self.dealer.won:
                self.console.print('Dealer won the round', style='red')
            elif self.draw:
                self.console.print('The round is a draw', style='yellow')
        else:
            self.console.print('Player went bankrupt! Game over!\n', style='red')
            self.console.print('New game!', style='blue')
            self.__init__()
            self.run()


    def print_player_hand(self):
        self.console.print(f'\nPlayer hand: {self.player.cards}')
        self.console.print(f'Player score: {self.player.score}\n')
        
    
    def print_dealer_hand(self, reveal=True):
        if reveal:
            self.console.print(f'Dealer hand: {self.dealer.cards}')
            self.console.print(f'Dealer score: {self.dealer.score}\n')
        else:
            self.console.print(f'Dealer hand: {[self.dealer.cards[0], "?"]}\n')


    def run(self):
        try:
            self.player.funds = int(input('\nPlease enter your starting funds.\n>>> '))
            if self.player.funds <= 0:
                self.console.print('\nInvalid amount. Starting funds must be an integer greater than 0.', style='red')
                self.run()
        except EOFError:
            exit('\nExiting game...\n')
        except ValueError:
            self.console.print('\nInvalid amount. Starting funds must be an integer greater than 0.', style='red')
            self.run()

        while True:
            try:
                cmd = input(f'\nYou have ${self.player.funds}. How much would you like to bet?\n>>> ')
                if cmd in ['exit', 'quit']:
                    exit('\nExiting game...\n')
                else:
                    self.player.bet = int(cmd)
                    if self.player.bet <= 0:
                        self.console.print('\nInvalid bet. Amount must be greater than 0.', style='red')
                        continue
                    elif self.player.bet > self.player.funds:
                        self.console.print('\nInvalid bet. Amount must be within your betting range.', style='red')
                        continue
            except EOFError:
                exit('\nExiting game...\n')
            except ValueError:
                self.console.print('\nInvalid bet. Enter an integer within your betting range.', style='red')
                continue

            self.place_bets()
            self.print_player_hand()
            self.print_dealer_hand(reveal=False)
            self.get_player_input()


if __name__ == '__main__':
    game = Blackjack()
    game.run()
