from tkinter import *
from PIL import ImageTk, Image
from CardsController import *
from enum import Enum
class Player:
    _cards = list()
    _cardImg = None    #image that is shown for the player
    _card_label = None #card label is the container of the cardImg

    def __init__(self, cards, parentWidget, row, column):
        self._cards = cards

        cardsController = CardsController.get_cards_controller()
        self._cardImg = ImageTk.PhotoImage(cardsController.get_back_card().get_image())
        self._card_label = Label(parentWidget, text='', image=self._cardImg, compound='center')
        self._card_label.configure(bg='green')
        self._card_label.grid(row=row, column=column, sticky='WE', padx=50, pady=50)

    def update_card_image(self):
        if len(self._cards) == 0:
            return None

        self._cardImg = ImageTk.PhotoImage(self._cards[0].get_image())
        self._card_label.configure(image=self._cardImg, bg='green')

    def set_back_card_image(self):
        cardsController = CardsController.get_cards_controller()
        self._cardImg = ImageTk.PhotoImage(cardsController.get_back_card().get_image())
        self._card_label.configure(image=self._cardImg, bg='green')

    def set_loser_card_image(self):
        cardsController = CardsController.get_cards_controller()
        self._cardImg = ImageTk.PhotoImage(cardsController.get_loser_card().get_image())
        self._card_label.configure(image=self._cardImg, bg='green')

    def remove_image(self):
        self._cardImg = ''
        self._card_label.configure(image=self._cardImg, bg='green')

    def set_winner_card_image(self):
        cardsController = CardsController.get_cards_controller()
        self._cardImg = ImageTk.PhotoImage(cardsController.get_winner_card().get_image())
        self._card_label.configure(image=self._cardImg, bg='green')

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

class GamePhase:
    ProcessWar = 0,
    ShowCards = 1,
    InitGame = 2

win = Tk()

win.iconbitmap('icon.ico')
win.title('War Card Game')
win.config(bg='green')

num_of_players = 2

war = War()

players = []

#create next move button
button = Button(win)
button.grid(row=2, column=1, padx=50, pady=50)

#create gameStats text
gameStatsString = StringVar()
gameStatsString.set("")
gameStatsLabel = Label(win, textvariable=gameStatsString)
gameStatsLabel.grid(row=1, column=1)
gameStatsLabel.configure(bg='green', font = ('calibri', 15, 'bold'))

def initGame():
    global win, gameStatsString, players, num_of_players, gamePhase

    cardsController = CardsController.get_cards_controller()

    #get num_of_players random decks
    decks = cardsController.get_splited_decks(num_of_players)

    # reset players in case they were already created
    players = []

    player1 = Player(decks[0], win, 1, 0)
    players.append(player1)

    player2 = Player(decks[1], win, 1, 2)
    players.append(player2)

    war.cards = []
    war.num_of_moves_until_end = 0

    gameStatsString.set("")

    gamePhase = GamePhase.ShowCards

def end_game():
    global button, gamePhase, players, war
    button.configure(text="Play again!")

    winnerIndex = -1
    for i in range(0, len(players)):
        playerCard = players[i].get_first_card()
        if playerCard is not None:
            winnerIndex = i

    if winnerIndex == -1:
        gameStatsString.set("Game ended! Draw!")
    else:
        gameStatsString.set("Player " + str(winnerIndex) + " won the game!")

    for i in range(0, len(players)):
        if i == winnerIndex:
            players[i].set_winner_card_image()

        if i != winnerIndex:
            players[i].set_loser_card_image()

        if winnerIndex == -1:
            players[i].set_back_card_image()

    gamePhase = GamePhase.InitGame

def process_move():
    global button, gamePhase, players, war

    #get the biggest card from the game
    biggest_card_number = -1
    for i in range(0, len(players)):
        playerCard = players[i].get_first_card()

        if playerCard is None:
            continue

        if playerCard.get_number() > biggest_card_number:
            biggest_card_number = playerCard.get_number()

    if gamePhase == GamePhase.InitGame:
        initGame()
        return

    # game should end if one card is None (one player lost a card)
    gameShouldEnd = False
    for i in range(0, len(players)):
        playerCard = players[i].get_first_card()

        if playerCard is None:
            gameShouldEnd = True

    if gameShouldEnd:
        end_game()
        return

    if gamePhase == GamePhase.ProcessWar:
        if war.num_of_moves_until_end > 0:
            # currently in a war. Just remove the cards and show the new ones

            for i in range(0, len(players)):
                playerCard = players[i].get_first_card()
                # move the first card from the player to the war cards
                war.cards.append(playerCard)
                players[i].pop_card()

            for i in range(0, len(players)):
                players[i].update_card_image()

            war.num_of_moves_until_end -= 1

            for i in range(0, len(players)):
                if players[i].get_first_card() == None:
                    war.num_of_moves_until_end = 0

            gameStatsString.set("War! cards left to drop:" + str(war.num_of_moves_until_end))

            gamePhase = GamePhase.ProcessWar
            return

        if war.num_of_moves_until_end == 0:
            # if multiple players have the biggest card we need to start the war

            # count how many players have the biggest card
            num_of_players_with_biggest_card = 0
            for i in range(0, len(players)):
                playerCard = players[i].get_first_card()

                if playerCard.get_number() == biggest_card_number:
                    num_of_players_with_biggest_card += 1

            # we found multiple players that has the same biggest card. We need to start a war!
            if num_of_players_with_biggest_card >= 2:
                if biggest_card_number == 14:
                    # for ace, set war moves to 11
                    war.num_of_moves_until_end = 11
                else:
                    # set war moves to biggest_card_number
                    war.num_of_moves_until_end = biggest_card_number

                gameStatsString.set("War! cards left to drop:" + str(war.num_of_moves_until_end))

                gamePhase = GamePhase.ProcessWar
                return

            # we dont need to do a war. Just a single player is the winner
            if num_of_players_with_biggest_card == 1:
                winnerIndex = -1

                for i in range(0, len(players)):
                    playerCard = players[i].get_first_card()

                    if playerCard.get_number() == biggest_card_number:
                        winnerIndex = i

                    # move the first card from the player to the war cards
                    war.cards.append(playerCard)
                    players[i].pop_card()

                for i in range(0, len(players)):
                    if i == winnerIndex:
                        gameStatsString.set("Player: " + str(i) + " won the cards")

                        #move the cards from the war to the winner player
                        for warCard in war.cards:
                            players[i].add_card(warCard)

                        #reset war cards because now the winner have them
                        war.cards = []

                        gamePhase = GamePhase.ShowCards
                    else:
                        players[i].set_back_card_image()
                return

    if gamePhase == GamePhase.ShowCards:
        # in case the button had previously another text value, reset it to next move
        button.configure(text="Next move")

        # in case we don't have a war in progress, reset the stats to nothing
        if war.num_of_moves_until_end == 0:
            gameStatsString.set("")

        for i in range(0, len(players)):
            players[i].update_card_image()

        # when the user will press again the nextMove button, we will process the war
        gamePhase = GamePhase.ProcessWar
        return

initGame()

button.configure(text="Next move", command=process_move, font = ('calibri', 15, 'bold'), borderwidth = '4')

win.resizable(False, False)
win.mainloop()