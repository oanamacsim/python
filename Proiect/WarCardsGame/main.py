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

    def get_is_in_war(self):
        return self._is_in_war

    def add_card(self, to_add: Card):
        self._cards.append(to_add)

    def pop_card(self) -> Card:
        del self._cards[0]

    def get_cards(self):
        return self._cards

    def get_first_card(self) -> Card:
        if len(self._cards) == 0:
            return None
        return self._cards[0]

class War:
    cards = list()
    num_of_moves_until_end = 0
    num_of_players = 0

    def is_war_in_progress(self):
        return self.num_of_players >= 2

class GamePhase:
    GameJustStarted = 1,
    InitWar = 2,
    ProcessWar = 3,
    ShowCards = 4,

cardsController = CardsController.get_cards_controller()

num_of_players = 4
decks = cardsController.get_splited_decks(num_of_players)

players = []

war = War()
gamePhase = GamePhase.ShowCards

for i in range(0, num_of_players):
    player = Player(decks[i],win, 1, i)
    players.append(player)

def process_move():
    global gamePhase, players, war
    print(war.num_of_moves_until_end)
    print("-------------------")
    for i in range(0, len(players)):
        stringList = []
        for j in range(0, len(players[i].get_cards())):
            stringList.append(players[i].get_cards()[j].id)
        print("Player{}: {}".format(i, stringList))

    print("-------------------")

    biggest_card_number = -1
    for i in range(0, len(players)):
        playerCard = players[i].get_first_card()

        if war.is_war_in_progress():
            if players[i].get_is_in_war():
                if playerCard.get_number() > biggest_card_number:
                    biggest_card_number = playerCard.get_number()
        else:
            if playerCard.get_number() > biggest_card_number:
                biggest_card_number = playerCard.get_number()

    if gamePhase == GamePhase.InitWar:
        # init war
        print("Init War")
        for i in range(0, len(players)):
            playerCard = players[i].get_first_card()
            war.cards.append(playerCard)

            if playerCard.get_number() == biggest_card_number:
                players[i].set_is_in_war(True)
                players[i].update_card_text("IN WAR")
                war.num_of_players += 1
            else:
                players[i].set_is_in_war(False)
                players[i].update_card_text("NOT IN WAR")
                players[i].set_back_card_image()
                players[i].pop_card()

        gamePhase = GamePhase.ProcessWar

        if war.num_of_players >= 2:
            # we have at least 2 players in this war
            war._num_of_moves_until_end = biggest_card_number
            return
        else:
            # we can process war results directly in this frame
            war._num_of_moves_until_end = 0

    if gamePhase == GamePhase.ProcessWar:
        print("Process War")
        if war._num_of_moves_until_end == 0:
            war.num_of_players = 0
            for i in range(0, len(players)):
                playerCard = players[i].get_first_card()

                if players[i].get_is_in_war():
                    if playerCard.get_number() == biggest_card_number:
                        war.num_of_players += 1
                    else:
                        players[i].set_is_in_war("False")
                        war.num_of_players -= 1

                player.pop_card()

        if war._num_of_moves_until_end > 0:
            for i in range(0, len(players)):
                if players[i].get_is_in_war():
                    players[i].pop_card()
                    players[i].update_card_image()
            war._num_of_moves_until_end -= 1

        if war.num_of_players == 1:
            for i in range(0, len(players)):
                if players[i].get_is_in_war():
                    # player i is the winner of this war
                    for warRewardCard in war.cards:
                        players[i].add_card(warRewardCard)

                    print("Player {} won {} cards".format(i, len(war.cards)))
                    players[i].set_is_in_war("False")

            # reset war
            war.cards = []
            war.num_of_players = 0
            war._num_of_moves_until_end = 0
            gamePhase = GamePhase.ShowCards

        return

    if gamePhase == GamePhase.ShowCards:
        print("Show Cards")
        for i in range(0, len(players)):
            players[i].update_card_image()
            players[i].update_card_text('')

            gamePhase = GamePhase.InitWar
        return

button = Button(win, text ="Next move", command=process_move)
button.grid(row=2, column=2, padx=50, pady=50)

playerScore = 0
cpuScore = 0

win.mainloop()