# png resources are downloaded from https://code.google.com/archive/p/vector-playing-cards/downloads into the /cards/ directory
from PIL import ImageTk, Image
import random

class Card:
    __number = None
    __type = None
    __image = None

    def __init__(self, number, type, imagePath):
        self.__number = int(number)
        self.__type = type
        self.id = number + type

        #to do: check if image exists
        self.__image = Image.open(imagePath)
        self.__image = self.__image.resize((250, 363))

    def get_number(self):
        return self.__number

    def get_type(self):
        return self.__type

    def get_image(self):
        return self.__image

class CardsController:
    __instance = None
    __cards = None

    _card_back = None

    __resourcesDir = "cards/"
    __cards_numbers = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]
    __cards_types = ["clubs", "diamonds", "hearts", "spades"]
    __card_back_path = "cards/card_back.png"

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
        return self.__cards

    def get_back_card(self):
        return self._card_back

    def __get_random_deck(self, num_of_changes, num_of_cards_to_remove):
        random_cards = self.__cards

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

        random_deck = self.__get_random_deck(10000, num_of_cards_to_remove)

        decks = []

        for i in range(0, num_of_decks):
            decks.append(list())

        for i in range(0, len(random_deck)):
            decks[i % num_of_decks].append(random_deck[i])

        return decks

    def __load_cards(self):
        self.__cards = []

        for cardNum in self.__cards_numbers:
            for cardType in self.__cards_types:
                imagePath = self.__resourcesDir + cardNum + "_of_" + cardType + ".png"
                self.__cards.append(Card(cardNum, cardType, imagePath))

        self._card_back = Card("-1", "None", self.__card_back_path)