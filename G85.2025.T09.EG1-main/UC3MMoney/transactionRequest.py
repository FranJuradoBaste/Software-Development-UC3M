import json



class transactionRequest:
    def __init__(self, IbAnFROM,iBaNtO, RECEpTorName):
        self.__receptorNaMe = RECEpTorName
        self.__IBANFrOm = IbAnFROM
        self.__IBANtO = iBaNtO



    def __str__(self):
        return "TransactionRequest:" + json.dumps(self.__dict__)

    @property
    def receptorNaMe(self):
        return self.__receptorNaMe
    @receptorNaMe.setter
    def receptorNaMe(self, value):
        self.__receptorNaMe = value

    @property
    def IBAN_FROM(self):
        return self.__IBANFrOm
    @IBAN_FROM.setter
    def IBAN_FROM(self, value):
        self.__IBANFrOm = value

    @property
    def IBAN_TO(self):
        return self.__IBANtO
    @IBAN_TO.setter
    def IBAN_TO(self, value):
        self.__IBANtO = value
