import json
from .transactionManagementException import transactionManagementException
from .transactionRequest import transactionRequest

class TransactionManager:
    def __init__(self):
        pass

    @staticmethod
    def validate_iban(iban):
        #Valida que sea un str
        if not isinstance(iban, str):
            return False

        #Valida las mayúsculas y quita los espacios
        iban = iban.replace(" ", "").upper()

        #Valida que comienza con ES
        if not iban.startswith("ES"):
            return False

        #Valida la longitud del IBAN
        if len(iban) != 24:
            return False

        #Validacion de que los dígitos luego de ES
        if not iban[2:].isdigit():
            return False

        rearranged_iban = iban[4:] + iban[:4]

        numeric_iban = []
        for ch in rearranged_iban:
            if ch.isdigit():
                numeric_iban.append(str(ch)) # Mantiene los números iguales
            else:
                numeric_iban.append(str(ord(ch) - 55))  # Convierte letras

        numeric_iban = ''.join(numeric_iban)

        return int(numeric_iban) % 97 == 1


    def readproductcodefrom_json(self, fi):

        try:
            with open(fi, encoding='utf-8') as F:
                DATA = json.load(F)
        except FileNotFoundError as E:
            raise (transactionManagementException
                   ("Wrong file or file path")) from E
        except json.JSONDecodeError as E:
            raise (transactionManagementException
                   ("JSON Decode Error - Wrong JSON Format")) from E

        try:
            Tfrom = DATA["from"]
            Tto = DATA["to"]
            Toname = DATA["receptor_name"]
            req = transactionRequest(Tfrom,Tto,Toname)
        except KeyError as E:
            raise transactionManagementException("JSON Decode Error "
                   "- Invalid JSON Key") from E
        if not self.validate_iban(Tfrom) :
            raise transactionManagementException("Invalid FROM IBAN")
        if not self.validate_iban(Tto):
            raise transactionManagementException("Invalid TO IBAN")
        return req
