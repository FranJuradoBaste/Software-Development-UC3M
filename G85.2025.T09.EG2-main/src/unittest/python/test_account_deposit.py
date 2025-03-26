"""Test para validar ingresos"""

# pylint: disable=too-many-public-methods
# pylint: disable=too-many-lines
import unittest
import json
import os
from uc3m_money import AccountManager
from uc3m_money.account_management_exception import AccountManagementException
from freezegun import freeze_time

class MyTestCase(unittest.TestCase):
    """Test para validar un ingreso valido."""

    @classmethod
    def setUpClass(cls):
        cls.manager = AccountManager()
        cls.json_folder = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                       "..", "..", "JsonFiles"))

    @freeze_time("2025-05-23")
    def test_valid_tc1(self):
        """TC1 - Caso válido"""
        file_path = os.path.join(self.json_folder, "TC1.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({
                "IBAN": "ES9121000418450200051332",
                "AMOUNT": "EUR 123.45"
            }, f, indent=4) # type: ignore

        result = self.manager.deposit_into_account(file_path)
        expected_hash = "3814f093d40db77f64796fef98a0467e8516dbedf5ff918c85c7a61b5f436c52"
        self.assertEqual(result, expected_hash)

    @freeze_time("2025-05-23")
    def test_invalid_tc2(self):
        """TC2 - JSON vacío"""
        file_path = os.path.join(self.json_folder, "TC2.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")

        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)

        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc3(self):
        """TC3 - Duplicación del Nodo 1"""
        file_path = os.path.join(self.json_folder, "TC3.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
    {
        "IBAN": "ES9121000418450200051332",
        "AMOUNT": "EUR 123.45"
    }
    {
        "IBAN": "ES9121000418450200051332",
        "AMOUNT": "EUR 123.45"
    }
    ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc4(self):
        """TC4 - Borrado del Nodo 2"""
        file_path = os.path.join(self.json_folder, "TC4.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
    "IBAN": "ES9121000418450200051332",
    "AMOUNT": "EUR 123.45"
    }
    ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc5(self):
        """TC5 - Duplicación del Nodo 2"""
        file_path = os.path.join(self.json_folder, "TC5.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
    {{
        "IBAN": "ES9121000418450200051332",
        "AMOUNT": "EUR 123.45"
    }
    ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc6(self):
        """TC5 - Duplicación del Nodo 2"""
        file_path = os.path.join(self.json_folder, "TC6.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
        {}
        ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid input structure")

    @freeze_time("2025-05-23")
    def test_invalid_tc7(self):
        """TC5 - Duplicación del Nodo 2"""
        file_path = os.path.join(self.json_folder, "TC6.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
        {}
        ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid input structure")

    @freeze_time("2025-05-23")
    def test_invalid_tc8(self):
        """TC8 - Borrado del Nodo4"""
        file_path = os.path.join(self.json_folder, "TC8.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
               {
                   """IBAN""": """ES9121000418450200051332""",
                   """AMOUNT""": """EUR 123.45"""
               }
               ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc9(self):
        """TC9 - Duplicación del Nodo4"""
        file_path = os.path.join(self.json_folder, "TC9.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
               {
                   """IBAN""": """ES9121000418450200051332""",
                   """AMOUNT""": """EUR 123.45"""
               }}
               ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc10(self):
        """TC10 - Formato incorrecto en IBAN"""
        file_path = os.path.join(self.json_folder, "TC10.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
               {
                   "IBAN": "INVALID_IBAN",
                   "AMOUNT": "EUR 100.00"
               }
               ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR IBAN not valid")

    @freeze_time("2025-05-23")
    def test_invalid_tc11(self):
        """TC11 - Formato incorrecto en AMOUNT"""
        file_path = os.path.join(self.json_folder, "TC11.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
               {
                   ""IBAN"": ""ES9121000418450200051332""""IBAN"": ""ES9121000418450200051332"",
                    ""AMOUNT"": ""EUR 123.45""
               }
               ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc12(self):
        """Borrado del Nodo7"""
        file_path = os.path.join(self.json_folder, "TC12.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
               {""IBAN"": ""ES9121000418450200051332""
                    ""AMOUNT"": ""EUR 123.45""
               }
               ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc13(self):
        """Duplicación del Nodo7"""
        file_path = os.path.join(self.json_folder, "TC13.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
               { ""IBAN"": ""ES9121000418450200051332"",,
                    ""AMOUNT"": ""EUR 123.45""
               }
               ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc14(self):
        """Borrado del Nodo8"""
        file_path = os.path.join(self.json_folder, "TC14.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
               {  ""IBAN"": ""ES9121000418450200051332"",
               }
               ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc15(self):
        """Duplicación del Nodo8"""
        file_path = os.path.join(self.json_folder, "TC15.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {  ""IBAN"": ""ES9121000418450200051332"",
    "                  "AMOUNT"": ""EUR 123.45""""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc16(self):
        """Borrado del Nodo10"""
        file_path = os.path.join(self.json_folder, "TC16.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {   : ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc17(self):
        """Duplicación del Nodo10"""
        file_path = os.path.join(self.json_folder, "TC17.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {   ""IBAN""""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc18(self):
        """Borrado del Nodo11"""
        file_path = os.path.join(self.json_folder, "TC18.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {    ""IBAN"" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc19(self):
        """Duplicación del Nodo11"""
        file_path = os.path.join(self.json_folder, "TC19.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {     ""IBAN"::" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc20(self):
        """Borrado del Nodo12"""
        file_path = os.path.join(self.json_folder, "TC20.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {      ""IBAN"": ,
                         ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc21(self):
        """Duplicación del Nodo12"""
        file_path = os.path.join(self.json_folder, "TC21.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {       ""IBAN"": ""ES9121000418450200051332""""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc22(self):
        """Borrado del Nodo14"""
        file_path = os.path.join(self.json_folder, "TC22.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {       ""IBAN"": ""ES9121000418450200051332"",
                        : ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc23(self):
        """Duplicación del Nodo14"""
        file_path = os.path.join(self.json_folder, "TC23.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {       ""IBAN"": ""ES9121000418450200051332"",
                        : ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc24(self):
        """Borrado del Nodo15"""
        file_path = os.path.join(self.json_folder, "TC24.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {        ""IBAN"": ""ES9121000418450200051332"",
                            ""AMOUNT"" ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc25(self):
        """Duplicación del Nodo15"""
        file_path = os.path.join(self.json_folder, "TC25.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {        ""IBAN"": ""ES9121000418450200051332"",
                            ""AMOUNT"" ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc26(self):
        """Borrado del Nodo16"""
        file_path = os.path.join(self.json_folder, "TC26.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {         ""IBAN"": ""ES9121000418450200051332"",
                            ""AMOUNT"": 
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc27(self):
        """Duplicación del Nodo16"""
        file_path = os.path.join(self.json_folder, "TC27.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {          ""IBAN"": ""ES9121000418450200051332"",
                            ""AMOUNT"": ""EUR 123.45""""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc28(self):
        """Borrado del Nodo17"""
        file_path = os.path.join(self.json_folder, "TC28.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {           ""IBAN"": ""ES9121000418450200051332"",
                                ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc29(self):
        """Duplicación del Nodo17"""
        file_path = os.path.join(self.json_folder, "TC29.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  { ""IBAN"": ""ES9121000418450200051332"",
                    AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc30(self):
        """Borrado del Nodo18"""
        file_path = os.path.join(self.json_folder, "TC30.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {  """": ""ES9121000418450200051332"",
                    ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc31(self):
        """Duplicación del Nodo18"""
        file_path = os.path.join(self.json_folder, "TC31.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {  ""IBANIBAN"":"": ""ES9121000418450200051332"",
                    """"AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc32(self):
        """Borrado del Nodo19"""
        file_path = os.path.join(self.json_folder, "TC32.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {   ""IBAN: ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc33(self):
        """Duplicación del Nodo19"""
        file_path = os.path.join(self.json_folder, "TC33.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {     ""IBAN"""": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc34(self):
        """Borrado del Nodo21"""
        file_path = os.path.join(self.json_folder, "TC34.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {     ""IBAN"": ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc35(self):
        """Duplicación del Nodo21"""
        file_path = os.path.join(self.json_folder, "TC35.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {      ""IBAN"": """"ES9121000418450200051332"",
                            ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc36(self):
        """Borrado del Nodo22"""
        file_path = os.path.join(self.json_folder, "TC36.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                  {      ""IBAN"": """",
                            ""AMOUNT"": ""EUR 123.45""
                  }
                  ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc37(self):
        """Duplicación del Nodo22"""
        file_path = os.path.join(self.json_folder, "TC37.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     {       ""IBAN"": ""ES9121000418450200051332ES9121000418450200051332"",
                            ""AMOUNT"": ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc38(self):
        """Borrado del Nodo23"""
        file_path = os.path.join(self.json_folder, "TC38.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     {        ""IBAN"": ""ES9121000418450200051332,
                            ""AMOUNT"": ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc39(self):
        """Duplicación del Nodo23"""
        file_path = os.path.join(self.json_folder, "TC39.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     {        ""IBAN"": ""ES9121000418450200051332"""",
                                ""AMOUNT"": ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc40(self):
        """Borrado del Nodo24"""
        file_path = os.path.join(self.json_folder, "TC40.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     { ""IBAN"": ""ES9121000418450200051332"",
                        AMOUNT"": ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc41(self):
        """Duplicación del Nodo24"""
        file_path = os.path.join(self.json_folder, "TC41.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     {   ""IBAN"": ""ES9121000418450200051332"",
                            """"AMOUNT"": ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc42(self):
        """Borrado del Nodo25"""
        file_path = os.path.join(self.json_folder,"TC42.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     {"""IBAN"": ""ES9121000418450200051332"",
    "                  """: ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc43(self):
        """Duplicado del Nodo25"""
        file_path = os.path.join(self.json_folder,"TC43.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     { ""IBAN"": ""ES9121000418450200051332"",
                      ""AMOUNTAMOUNT"": ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc44(self):
        """Borrado del Nodo26"""
        file_path = os.path.join(self.json_folder,"TC44.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT: ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc45(self):
        """Duplicadoo del Nodo26"""
        file_path = os.path.join(self.json_folder,"TC45.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"""": ""EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc46(self):
        """Borrado del Nodo28"""
        file_path = os.path.join(self.json_folder,"TC46.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                     {  ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": EUR 123.45""
                     }
                     ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")


    @freeze_time("2025-05-23")
    def test_invalid_tc47(self):
        """Duplicado del Nodo28"""
        file_path = os.path.join(self.json_folder, "TC47.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": """"EUR 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc48(self):
        """Borrado del Nodo29"""
        file_path = os.path.join(self.json_folder, "TC48.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": """"
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc49(self):
        """Duplicado del Nodo29"""
        file_path = os.path.join(self.json_folder, "TC49.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      {""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45EUR 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc50(self):
        """Borrado del Nodo30"""
        file_path = os.path.join(self.json_folder, "TC50.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc51(self):
        """Duplicado del Nodo30"""
        file_path = os.path.join(self.json_folder, "TC51.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc52(self):
        """Borrado del Nodo35"""
        file_path = os.path.join(self.json_folder, "TC52.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc53(self):
        """Duplicado del Nodo35"""
        file_path = os.path.join(self.json_folder, "TC53.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ESES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")
    @freeze_time("2025-05-23")
    def test_invalid_tc54(self):
        """Borrado del Nodo36"""
        file_path = os.path.join(self.json_folder, "TC54.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      {""IBAN"": ""ES"",
                        ""AMOUNT"": ""EUR 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc55(self):
        """Duplicado del Nodo36"""
        file_path = os.path.join(self.json_folder, "TC55.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      {""IBAN"": ""ES91210004184502000513329121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc56(self):
        """Borrado del Nodo42"""
        file_path = os.path.join(self.json_folder, "TC56.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      {  ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": "" 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc57(self):
        """Duplicado del Nodo42"""
        file_path = os.path.join(self.json_folder, "TC57.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      {""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUREUR 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc58(self):
        """Borrado del Nodo43"""
        file_path = os.path.join(self.json_folder, "TC58.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR ""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc59(self):
        """Duplicado del Nodo43"""
        file_path = os.path.join(self.json_folder, "TC59.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR123.45123.45 ""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc60(self):
        """Borrado del Nodo44"""
        file_path = os.path.join(self.json_folder, "TC60.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 12345""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc61(self):
        """Duplicado del Nodo44"""
        file_path = os.path.join(self.json_folder, "TC61.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      { ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123..45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc62(self):
        """Borrado del Nodo45"""
        file_path = os.path.join(self.json_folder, "TC62.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      {   ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc63(self):
        """Duplicado del Nodo45"""
        file_path = os.path.join(self.json_folder, "TC63.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      {""IBAN"" :""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.4545""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc64(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC64.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''
                      {#
                        ""IBAN"" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                      }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc65(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC65.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                       ""IBAN"": ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                        }#
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc66(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC66.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                         ""IBAN"": ""ES9121000418450200051332"",#
                            ""AMOUNT"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc67(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC67.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                          ""IBAN"":# ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc68(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC68.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                       ""IBAN"" ""ES9121000418450200051332"",
                        ""AMOUNT"":# ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc69(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC69.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                        ""#IBAN"" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc70(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC70.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                        ""IBAN#"" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc71(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC71.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                          ""IBAN""# ""ES9121000418450200051332"",
                            ""AMOUNT"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc72(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC72.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                          ""IBAN"" ""#ES9121000418450200051332"",
                            ""AMOUNT"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc73(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC73.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                           ""IBAN"" ""ES9121000418450200051332""#,
                            ""AMOUNT"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc74(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC74.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                        ""IBAN"" ""ES9121000418450200051332"",
                        ""#AMOUNT"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc75(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC75.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                         ""IBAN"" ""ES9121000418450200051332"",
                         ""AMOUNT#"": ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc76(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC76.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                           ""IBAN"" ""ES9121000418450200051332"",
                            ""AMOUNT""#: ""EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc77(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC77.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{
                           ""IBAN"" ""ES9121000418450200051332"",
                            ""AMOUNT"": ""#EUR 123.45""
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc78(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC78.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{""IBAN"" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45""#
                        }
                      ''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc79(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC78.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{ ""IBAN"" ""ES#9121000418450200051332"",
                    ""AMOUNT"": ""EUR 123.45" }''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc80(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC80.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{  ""IBAN"" ""ES9121000418450200051332#"",
                            ""AMOUNT"": ""EUR 123.45""}''')
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc81(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC81.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{""IBAN"" ""ES9121000418450200051332#"",
                        ""AMOUNT"": ""EUR 123.45""
                            }''')

        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc82(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC82.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{""IBAN"" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123#.45""
                            }''')

        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc83(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC83.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{""IBAN"" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.#45""
                            }''')

        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

    @freeze_time("2025-05-23")
    def test_invalid_tc84(self):
        """Modificado"""
        file_path = os.path.join(self.json_folder, "TC84.json")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write('''{""IBAN"" ""ES9121000418450200051332"",
                        ""AMOUNT"": ""EUR 123.45#""
                            }''')

        with self.assertRaises(AccountManagementException) as cm:
            self.manager.deposit_into_account(file_path)
        self.assertEqual(str(cm.exception), "ERROR invalid JSON format")

if __name__ == '__main__':
    unittest.main()
