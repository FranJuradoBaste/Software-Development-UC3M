
import string
from UC3MMoney import TransactionManager


#GLOBAL VARIABLES
LETTERS = string.ascii_letters + string.punctuation + string.digits

SHIFT = 3



def Encode(word):
    ENCODED = ""
    for LETTER in word:
        if LETTER == ' ':
            ENCODED = ENCODED + ' '
        else:
            X = (LETTERS.index(LETTER) + SHIFT) % len(LETTERS)
            ENCODED = ENCODED + LETTERS[X]
    return ENCODED

def Decode(word):
    Encoded = ""
    for Letter in word:
        if Letter == ' ':
            Encoded = Encoded + ' '
        else:
            X= (LETTERS.index(Letter) - SHIFT) % len(LETTERS)
            Encoded = Encoded + LETTERS[X]
    return Encoded

def Main():

    Mng = TransactionManager()
    Res = Mng.readproductcodefrom_json("test.json")
    StrRes = str(Res)
    print(StrRes)
    EncodeRes = Encode(StrRes)
    print("Encoded Res "+ EncodeRes)
    DecodeRes = Decode(EncodeRes)
    print("Decoded Res: " + DecodeRes)
    print("IBAN_FROM: " + Res.IBAN_FROM)
    print("IBAN_TO: " + Res.IBAN_TO)

if __name__ == "__main__":
    Main()
