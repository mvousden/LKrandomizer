import random
import randomizer
"""
Child class of Randomizer
"""


class BalancedRandomizer(randomizer.Randomizer):

    def __init__(self, seedVal, cardList):
        super().__init__(seedVal, cardList)
        self.rarityLists = dict()  # members: four lists of cards, one for each rarity level
        self.buildRarityLists()

    def writeRandomizationStyleToLog(self):
        self.optionLog += 'Balanced randomization style\n'

    def buildRarityLists(self):
        self.rarityLists = {1: list(),
                            2: list(),
                            3: list(),
                            4: list()}
        for card in self.cardList:
            self.rarityLists[card.rarity].append(card)

    def randomizeStartingDeck(self, fullRandomDeckList, balancedDeckList, asmDict):
        self.optionLog += 'Randomized starting deck\n'
        self.spoilerLog += 'Starting Deck: '
        for cardSlot in balancedDeckList:
            index = random.randint(0, len(cardSlot.replaceCardList) - 1)
            cardID = cardSlot.replaceCardList[index]
            card = self.getCardFromCardID(cardID)
            for address in cardSlot.addressList:
                self.outputDict[address] = card.cardID
            amount = str((len(cardSlot.addressList) - 1))
            self.spoilerLog += (card.cardName + ' x' + amount + '. ')  # print card name
        self.spoilerLog += '\n\n'

    def buildCardOutput(self, location):
        originalCard = self.getCardFromInteractID(location.originalInteractID)
        if originalCard is None:
            card = self.getRandomCard()
        else:
            card = self.getRandomCardFromRarity(originalCard.rarity)
        cardBytes = card.interactID
        if location.originalType == 3:  # originally item location
            # append card-get to interactID
            cardBytes += self.cardGetByte
        if location.originalType == 4:  # originally shayel key or wyht key
            self.outputDict[location.typeAddress] = self.cardGetByte
        self.outputDict[location.address] = cardBytes  # pair up location and card interact ID
        self.spoilerLog += (
                location.levelName + ' ' + location.description + ' has ' + card.cardName + '\n')  # (Level name) (location) has (card name)

    def randomizeWarriorWyhtCards(self, warriorWyhtList):
        self.spoilerLog += 'Warrior of Wyht cards:\n'
        for member in warriorWyhtList:
            originalCard = self.getCardFromCardID(member.value)
            card = self.getRandomCardFromRarity(originalCard.rarity)
            self.outputDict[member.address] = card.cardID
            self.spoilerLog += card.cardName + '. '  # print card name
        self.spoilerLog += '\n\n'

    def randomizeLevelBonusCards(self, levelBonusList):
        self.optionLog += 'Randomized level bonus cards\n'
        for levelBonusSlot in levelBonusList:
            originalCard = self.getCardFromCardID(levelBonusSlot.originalCardID)
            card = self.getRandomCardFromRarity(originalCard.rarity)
            for address in levelBonusSlot.addressList:
                self.outputDict[address] = card.cardID

    def randomizeShopCards(self, shopCardList):
        self.optionLog += 'Randomized shop cards\n'
        self.spoilerLog += 'Shop cards:\n'
        n = 0
        for shopCard in shopCardList:
            n += 1
            originalCard = self.getCardFromCardID(shopCard.value)
            card = self.getRandomCardFromRarity(originalCard.rarity)
            self.outputDict[shopCard.address] = card.cardID
            self.spoilerLog += card.cardName + '. '  # print card name
            if n % 10 == 0:  # every tenth card start new line
                self.spoilerLog += '\n'
        self.spoilerLog += '\n'

    def randomizeFairyCards(self, fairyCardList):
        self.optionLog += 'Randomized red fairy rewards\n'
        self.spoilerLog += 'Red fairy rewards:\n'
        for fairyCard in fairyCardList:
            originalCard = self.getCardFromCardID(fairyCard.value)
            card = self.getRandomCardFromRarity(originalCard.rarity)
            self.outputDict[fairyCard.address] = card.cardID
            self.spoilerLog += card.cardName + '. '  # print card name

    def getCardFromCardID(self, cardID):
        match = self.cardList[0]
        for card in self.cardList:
            if card.cardID == cardID:
                match = card
        return match

    def getCardFromInteractID(self, interactID):
        match = None
        for card in self.cardList:
            if card.interactID == interactID:
                match = card
        return match

    def getRandomCardFromRarity(self, rarity):
        if rarity in self.rarityLists.keys():  # choose from any card
            index = random.randint(0, len(self.rarityLists[rarity]) - 1)
            card = self.rarityLists[rarity][index]
        else:
            card = self.getRandomCard()
        return card
