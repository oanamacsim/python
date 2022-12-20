# png resources are downloaded from https://code.google.com/archive/p/vector-playing-cards/downloads into the /cards/ directory
from PIL import ImageTk, Image
import random

class Card:
    _number = None
    _type = None
    _image = None

    def __init__(self, number, type, imagePath):
        self._number = int(number)
        self._type = type
        self.id = number + type

        self._image = Image.open(imagePath)
        self._image = self._image.resize((250, 363))

    def get_number(self):
        return self._number

    def get_type(self):
        return self._type

    def get_image(self):
        return self._image


class CardsController:
    __instance = None
    _cards = None

    _card_back = None
    _card_loser = None

    _resourcesDir = "cards/"
    _cards_numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
    _cards_types = ["clubs", "diamonds", "hearts", "spades"]
    _card_back_path = "cards/card_back.png"
    _card_loser_path = "cards/card_loser.png"
    _card_winner_path = "cards/card_winner.png"

    @staticmethod
    def get_cards_controller():
        if CardsController.__instance is None:
            #init __instance by calling the constructor one single time
            CardsController()
        return CardsController.__instance

    def __init__(self):
        if CardsController.__instance:
            raise Exception("CardsController Singleton tried to be initialized twice. Aborting...")
        else:
            self.__load_cards()
            CardsController.__instance = self

    def get_cards(self):
        return self._cards

    def get_back_card(self):
        return self._card_back

    def get_loser_card(self):
        return self._card_loser

    def get_winner_card(self):
        return self.__card_winner

    def _get_random_deck(self, num_of_changes, num_of_cards_to_remove):
        random_cards = self._cards

        #remove first num_of_cards_to_remove (the smallest cards)
        for i in range(num_of_cards_to_remove):
            random_cards.pop(0)

        for i in range(0, num_of_changes):
            index1 = random.randint(0, len(random_cards) - 1)
            index2 = random.randint(0, len(random_cards) - 1)

            #swap the cards that are at the random indices
            tempCard = random_cards[index1]
            random_cards[index1] = random_cards[index2]
            random_cards[index2] = tempCard

        return random_cards

    def get_splited_decks(self, num_of_decks):
        num_of_cards_to_remove = 52 % num_of_decks

        random_deck = self._get_random_deck(10000, num_of_cards_to_remove)

        decks = []

        for i in range(0, num_of_decks):
            decks.append(list())

        for i in range(0, len(random_deck)):
            decks[i % num_of_decks].append(random_deck[i])

        # for i in range(0, len(decks)):
        #     for j in range(0, 23):
        #         decks[i].pop(0)

        return decks

    def __load_cards(self):
        self._cards = []

        for cardNum in self._cards_numbers:
            for cardType in self._cards_types:
                imagePath = self._resourcesDir + cardNum + "_of_" + cardType + ".png"
                self._cards.append(Card(cardNum, cardType, imagePath))

        self._card_back = Card("-1", "None", self._card_back_path)
        self._card_loser = Card("-1", "None", self._card_loser_path)
        self.__card_winner = Card("-1", "None", self._card_winner_path)