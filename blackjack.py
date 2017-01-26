class player(object):
    """This is the player class really"""
    def __init__(self,cash,bet = 0):
        self.__cards = []
        self.__initial_cash = cash
        self.__cash = cash
        self.__bet = bet

    def remove(self):
        self.__cards = []

    def bet(self,bet_amount):
        self.__cash = self.__cash-bet_amount
        self.__bet = bet_amount

    def bet_amount(self):
        return self.__bet

    def win(self):
        self.__cash = self.__cash + 2*self.__bet
        self.__bet = 0

    def tie(self):
        self.__cash = self.__cash + self.__bet
        self.__bet = 0

    def lose(self):
        self.__bet = 0

    def winnings(self):
        return self.__cash - self.__initial_cash

    def value(self):
        cards_no_ace = [x for x in self.__cards if x != "A"]
        aces_number = self.__cards.count("A")
        sum_1 = sum(cards_no_ace)+aces_number
        if aces_number >= 1:
            sum_2 = sum(cards_no_ace)+11+(aces_number-1)
        else:
            sum_2 = sum_1
        if sum_2 > 21:
            value = sum_1
        else:
            value = sum_2
        return value

    def receive(self,card):
        self.__cards.append(card)

    def __str__(self):
        return( " Your cards are:  "+str(self.__cards)+
                "\n Your currently have cash:  "+
                str(self.__cash)+
                "\n You are currently betting:  "+str(self.__bet))
    
    def cash(self):
        return(self.__cash)

class dealer(object):
    """This is the dealer class"""
    def __init__(self):
        self.__cards = []

    def remove(self):
        self.__cards = []

    def value(self):
        cards_no_ace = [x for x in self.__cards if x != "A"]
        aces_number = self.__cards.count("A")
        sum_1 = sum(cards_no_ace)+aces_number
        if aces_number >= 1:
            sum_2 = sum(cards_no_ace)+11+(aces_number-1)
        else:
            sum_2 = sum_1
        if sum_2 > 21:
            value = sum_1
        else:
            value = sum_2
        return value

    def __str__(self):
        return "The dealer's cards are:  "+str(self.__cards)

    def receive(self,card):
        self.__cards.append(card)
    

class shoe(object):
    """This is a shoe of cards class"""
    def __init__(self,number_decks,penetration):
        self.__number_decks = number_decks
        self.__penetration = penetration
        self.__cards = (["A",1,2,3,4,5,6,7,8,9]*4+[10]*16)*number_decks

    def shuffle(self):
        from random import shuffle
        return shuffle(self.__cards)

    def number(self):
        return len(self.__cards)

    def pop(self):
        return self.__cards.pop(0)

def deal(shoe,player):
    card = shoe.pop()
    player.receive(card)
    return card

def dealer_play(shoe,dealer):
    while dealer.value() < 17:
        card = deal(shoe,dealer)
        print("The dealer has been dealt：  ",card)
        print("The dealer's value is:  ", dealer.value())
    print("The dealer has finished playing.")


def play(shoe,player,dealer):
    n = input("How many decks do you want to play with:  ")
    p = input("Input penetration, e.g. for 75% enter 75:  ")
    cash = input("How much cash are you playing with, e.g. for £500 enter 500:  ")
    shoe = shoe(int(n),int(p))
    player = player(int(cash))
    dealer = dealer()
    print("Shuffling the shoe.")
    shoe.shuffle()
    print("Shuffle complete, let's begin.")
    
    while True:

        bet_amount = input("How much do you want to bet:  ")
        player.bet(int(bet_amount))
        card_1 = deal(shoe,dealer)
        print("The first card dealt to the dealer is:  ",card_1)
        card_2 = deal(shoe,player)
        print("You have been dealt:  ",card_2)
        card_3 = deal(shoe,dealer)
        print("The second card has been dealt to the dealer. ")
        card_4 = deal(shoe,player)
        print("You have been dealt:  ", card_4)
        if {card_1,card_3} == {10,"A"}:
            print("The dealer has a Blackjack.")
            if {card_2,card_4} == {10,"A"}:
                print("You also have a BlackJack, it's a push!")
                player.tie()
            else:
                print("But you don't have a Blackjack, you lose!")
                print("You lose your bet of:  ",player.bet_amount())
                player.lose()
        else:
            print("The dealer does not have a BlackJack.")
            if {card_2,card_4} == {10,"A"}:
                print("But you have a BlackJack, you win!")
                print("You win your bet of:  ",player.bet_amount())
                player.win()
            elif {card_2,card_4} != {10,"A"}:
                print("The dealer does not have Blackjack, the first card dealt to the dealer is:  ",card_1)
                TF = True
                while True:
                    print("This is your current status:  ")
                    print(player)
                    hs = input("Do you want to hit or stay, h/s:  ")
                    if hs == "s":
                       break
                    elif hs == "h":
                        card = deal(shoe,player)
                        print("You have been dealt:  ", card)
                        if player.value() > 21:
                            print("This is your current status:  ")
                            print(player)
                            print("You have gone bust and lose your bet of:  ", player.bet_amount())
                            player.lose()
                            TF = False
                            break
                if TF:
                    print("The second card dealt to the dealer is:  ",card_3)
                    print("The dealer is now playing, please wait.")
                    dealer_play(shoe,dealer)
                    print(dealer)
                    print("The dealer's value is:  ", dealer.value())
                    print("Your value is:  ", player.value())

                    if dealer.value() > 21:
                        print("The dealer has gone bust, you win!")
                        print("You win your bet of:  ", player.bet_amount())
                        player.win()
                    
                    elif dealer.value() > player.value():
                       print("The dealer has more value than you, you lose!")
                       print("You lose your bet of:  ", player.bet_amount())
                       player.lose()

                    elif dealer.value() < player.value():
                        print("The dealer has less value than you, you win!")
                        print("You win your bet of:  ", player.bet_amount())
                        player.win()

                    elif dealer.value() == player.value():
                        print("The dealer has the same value as you, it's a push!")
                        print("Your bet of:  ",player.bet_amount()," is returned to you.")
                        player.tie()
                        
        print("You currently have cash:  ", player.cash())
        yn = input("Do you want to play another round, y/n:  ")

        if yn == "y":
            player.remove()
            dealer.remove()
            if shoe.number() < 52*int(n)*(100-int(p))/100:
                shoe = shoe(n,p)
        else:
            winnings = player.winnings()
            break

    print("Thanks for playing, your total winnings are:  ", player.winnings())


