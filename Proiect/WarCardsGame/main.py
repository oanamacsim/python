from tkinter import *
from PIL import ImageTk, Image
from CardsController import *
from enum import Enum
win = Tk()

class Player:
    _cards = list()
    _cardImg = None
    _card_label = None
    _is_in_war = False

    def __init__(self, cards, parent, row, column):
        self._cards = cards
        self._is_in_war = False

        cardsController = CardsController.get_cards_controller()
        self._cardImg = ImageTk.PhotoImage(cardsController.get_back_card().get_image())
        self._card_label = Label(parent, text='', image=self._cardImg, compound='center')
        self._card_label.grid(row=row, column=column, sticky='WE', padx=50, pady=50)

    def update_card_image(self):
        if len(self._cards) == 0:
            self.set_back_card_image()
            return

        self._cardImg = ImageTk.PhotoImage(self._cards[0].get_image())
        self._card_label.configure(image=self._cardImg)

    def update_card_text(self, text: str):
        self._card_label.configure(text=text)

    def set_back_card_image(self):
        self._cardImg = ImageTk.PhotoImage(cardsController.get_back_card().get_image())
        self._card_label.configure(image=self._cardImg)

    def set_is_in_war(self, is_in_war: bool):
        self._is_in_war = is_in_war

    def add_card(self, to_add: Card):
        self._cards.append(to_add)

    def pop_card(self) -> Card:
        self._cards.pop(0)

    def get_first_card(self) -> Card:
        if len(self._cards) == 0:
            return None
        return self._cards[0]

class War:
    _cards = list()
    _num_of_moves_until_end = 0
    num_of_players = 0

    def start_war(self, cards: list, num_of_moves: int):
        self._cards = cards
        self._num_of_moves_until_end = num_of_moves
        self.num_of_players = 0

    def is_war_in_progress(self):
        return self._num_of_moves_until_end > 0

    def add_card_to_war(self, card):
        self._cards.append(card)

    def get_war_cards(self):
        return self._cards


class GamePhase:
    GameJustStarted = 1,
    ProcessWar = 2,
    TakeNewCards = 3,
    WarInProgress = 4,

cardsController = CardsController.get_cards_controller()

num_of_players = 4
decks = cardsController.get_splited_decks(num_of_players)

players = []

war = War()
gamePhase = GamePhase.GameJustStarted

for i in range(0, num_of_players):
    player = Player(decks[i],win, 1, i)
    players.append(player)

def process_move():
    global gamePhase, players, war

    if gamePhase == GamePhase.GameJustStarted:
        for i in range(0, len(players)):
            players[i].update_card_image()

        gamePhase = GamePhase.ProcessWar
        return

    biggest_card_number = -1
    for i in range(0, len(players)):
        playerCard = players[i].get_first_card()
        if playerCard.get_number() > biggest_card_number:
            biggest_card_number = playerCard.get_number()

    if gamePhase == GamePhase.ProcessWar:
        if war.is_war_in_progress() is False:
            # init war
            for i in range(0, len(players)):
                playerCard = players[i].get_first_card()
                if playerCard.get_number() == biggest_card_number:
                    players[i].set_is_in_war(True)
                    war.num_of_players += 1
                else:
                    players[i].set_is_in_war(False)
                    players[i].update_card_text('Lost')

        for i in range(0, len(players)):
            playerCard = players[i].get_first_card()
            if playerCard.get_number() == biggest_card_number:
                players[i].update_card_text('Won')
            else:
                players[i].update_card_text('Lost')

        gamePhase = GamePhase.TakeNewCards
        return

    if gamePhase == GamePhase.TakeNewCards:
        for i in range(0, len(players)):
            playerCard = players[i].pop_card()
            players[i].update_card_image()
            players[i].update_card_text('')
        gamePhase = GamePhase.ProcessWar
        return


    for i in range(0, len(players)):
        playerCard = players[i].get_first_card()
        if playerCard.get_number() == biggest_card_number:
            player.set_is_in_war(True)


    for i in range(0, len(players)):
        playerCard = players[i].pop_card()

        if playerCard == None:
            print("Game ended for this Player")
            continue

        players[i].update_card_image()

button = Button(win, text ="Next move", command=process_move)
button.grid(row=2, column=2, padx=50, pady=50)

playerScore = 0
cpuScore = 0

win.mainloop()
