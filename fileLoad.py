import os
import classes


class FileLoad:
    # file names
    cardIDFile = 'data/cardID.csv'
    itemIDFile = 'data/itemID.csv'
    startingDeckFullRandomFile = 'data/startingDeckAddressFullRandom.csv'
    startingDeckBalancedFile = 'data/startingDeckAddressBalanced.csv'
    startingInventoryASMFile = 'data/startingInventoryHex.txt'
    startingInventoryAddress = int(b'78908', 16)
    startingInventoryAdditionalASMFile = 'data/startingInventoryAdditionalHex.txt'
    startingInventoryAdditionalAddress = int(b'129810', 16)
    chestCardItemFile = 'data/chestCardItem.csv'
    warriorWyhtFile = 'data/warriorWyhtAddress.csv'
    levelBonusCardFile = 'data/levelBonusAddress.csv'
    shopCardFile = 'data/shopCardAddress.csv'
    fairyCardFile = 'data/fairyCardAddress.csv'
    enemyAttributeFile = 'data/enemyAttributeAddress.txt'
    deckPointFile = 'data/deckPointAddress.txt'
    lk2CardFile = 'data/lk2Card.csv'
    lk2EnemyFile = 'data/lk2Enemy.csv'
    savedPathFile = 'data/savedPath.txt'

    # constants
    isoSize = 1459978240
    gameID = bytes(b'GRNE52')

    def __init__(self):
        self.cardList = list()  # member: Card object
        self.loadCards()
        self.itemList = list()  # member: Item object
        self.loadItems()
        self.startingDeckFullRandomList = list()  # member: list() of two address
        self.loadStartingDeckFullRandom()
        self.startingDeckBalancedList = list()  # member: StartingDeckSlot object
        self.loadStartingDeckBalanced()
        self.startingInventoryASMDict = dict()  # key: .iso address, value: asm code in hex
        self.loadStartingInventoryASM()
        self.chestCardItemList = list()  # member: Location object
        self.loadChestCardItem()
        self.warriorWyhtList = list()  # member: AddressValue
        self.loadWarriorWyht()
        self.levelBonusList = list()  # member: LevelBonusSlot object
        self.loadLevelBonusCards()
        self.shopCardList = list()  # member: AddressValue object
        self.loadShopCards()
        self.fairyCardList = list()  # member: AddressValue object
        self.loadFairyCards()
        self.enemyAttributeList = list()  # member: .iso address
        self.loadEnemyAttributes()
        self.deckPointList = list()  # member: .iso address
        self.loadDeckPoints()
        self.lk2CardChangeList = list()  # member: AddressValue object
        self.loadlk2CardChanges()
        self.lk2EnemyChangeList = list()  # member: AddressValue object
        self.loadlk2EnemyChanges()

    def loadSavedFilePath(self):
        with open(self.savedPathFile, 'r') as file:
            savedPath = file.read()
        return savedPath

    def isGoodISO(self, ISOPath):
        if os.path.getsize(ISOPath) != self.isoSize:
            return False
        with open(ISOPath, 'rb') as iso_file:
            if iso_file.read(6) != self.gameID:
                return False
        return True

    def loadCards(self):
        # load [card ID, interact ID, card name, rarity] from file into cards list
        with open(self.cardIDFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = int(line[0], 16)
                line[0] = line[0].to_bytes(1, byteorder='big')
                line[1] = int(line[1], 16)
                line[1] = line[1].to_bytes(1, byteorder='big')
                line[3] = int(line[3])
                card = classes.Card(line[0], line[1], line[2], line[3])
                self.cardList.append(card)

    def loadItems(self):
        # load [item ID, card name] from file into cards list
        with open(self.itemIDFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = int(line[0], 16)
                line[0] = line[0].to_bytes(1, byteorder='big')
                item = classes.Item(line[0], line[1])
                self.itemList.append(item)

    def loadStartingDeckFullRandom(self):
        with open(self.startingDeckFullRandomFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = int(line[0], 16)
                line[1] = int(line[1], 16)
                self.startingDeckFullRandomList.append(line)

    def loadStartingDeckBalanced(self):
        with open(self.startingDeckBalancedFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                addressList = line[0].split('.')
                newAddressList = list()
                for address in addressList:
                    address = int(address, 16)
                    newAddressList.append(address)
                replaceList = line[1].split('.')
                newReplaceList = list()
                for replacement in replaceList:
                    replacement = int(replacement, 16)
                    replacement = replacement.to_bytes(1, byteorder='big')
                    newReplaceList.append(replacement)
                startingDeckSlot = classes.StartingDeckSlot(newAddressList, newReplaceList)
                self.startingDeckBalancedList.append(startingDeckSlot)

    def loadStartingInventoryASM(self):
        with open(self.startingInventoryASMFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = int(line, 16)
                line = line.to_bytes(4, byteorder='big')
                self.startingInventoryASMDict[self.startingInventoryAddress] = line
                self.startingInventoryAddress += 4
        with open(self.startingInventoryAdditionalASMFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = int(line, 16)
                line = line.to_bytes(4, byteorder='big')
                self.startingInventoryASMDict[self.startingInventoryAdditionalAddress] = line
                self.startingInventoryAdditionalAddress += 4

    def loadChestCardItem(self):
        # load [.iso address, type, area, level name, location desc, originalInteractID, typeAddress(optional)] from file into locations list
        with open(self.chestCardItemFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = int(line[0], 16)
                line[1] = int(line[1])
                line[2] = int(line[2])
                line[5] = int(line[5], 16)
                line[5] = line[5].to_bytes(1, byteorder='big')
                if not line[6] == '':  # has type address
                    line[6] = int(line[6], 16)
                    location = classes.Location(line[0], line[1], line[2], line[3], line[4], line[5], line[6])
                else:
                    location = classes.Location(line[0], line[1], line[2], line[3], line[4], line[5])
                self.chestCardItemList.append(location)

    def loadWarriorWyht(self):
        self.loadAddressValueFile(self.warriorWyhtFile, self.warriorWyhtList, 16, 1)

    def loadLevelBonusCards(self):
        # load [multiple .iso address seperated by '.', original cardID
        with open(self.levelBonusCardFile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                addressList = line[0].split('.')
                newAddressList = list()
                for address in addressList:
                    address = int(address, 16)
                    newAddressList.append(address)
                line[1] = int(line[1], 16)
                line[1] = line[1].to_bytes(1, byteorder='big')
                levelBonusSlot = classes.LevelBonusSlot(newAddressList, line[1])
                self.levelBonusList.append(levelBonusSlot)

    def loadShopCards(self):
        self.loadAddressValueFile(self.shopCardFile, self.shopCardList, 16, 1)

    def loadFairyCards(self):
        self.loadAddressValueFile(self.fairyCardFile, self.fairyCardList, 16, 1)

    def loadEnemyAttributes(self):
        self.loadAddressTxtFile(self.enemyAttributeFile, self.enemyAttributeList)

    def loadDeckPoints(self):
        self.loadAddressTxtFile(self.deckPointFile, self.deckPointList)

    def loadlk2CardChanges(self):
        self.loadAddressValueFile(self.lk2CardFile, self.lk2CardChangeList, 10, 1)

    def loadlk2EnemyChanges(self):
        self.loadAddressValueFile(self.lk2EnemyFile, self.lk2EnemyChangeList, 10, 2)

    def loadAddressTxtFile(self, fileName, intoList):
        with open(fileName, 'r') as file:
            lines = file.readlines()
            for address in lines:
                address = address.rstrip('\r\n')
                address = int(address, 16)
                intoList.append(address)

    def loadAddressValueFile(self, fileName, intoList, numSystem, numBytes):
        """

        :param fileName: file to read (str)
        :param intoList: list to save to (list)
        :param numSystem: how value is represented in file. 10 for deciaml, 16 for hexadecimal (int)
        :param numBytes: size of value (int)
        """
        with open(fileName, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip('\r\n')
                line = line.split(',')
                line[0] = int(line[0], 16)
                line[1] = int(line[1], numSystem)
                line[1] = line[1].to_bytes(numBytes, byteorder='big')  # values have lengths of two bytes
                addressValue = classes.AddressValue(line[0], line[1])
                intoList.append(addressValue)
