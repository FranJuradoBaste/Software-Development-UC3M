"""Tests unitarios para validar las transferencias bancarias (TC1 a TC23)."""
# pylint: disable=too-many-public-methods

import unittest
import json
import os
from uc3m_money import AccountManager
from uc3m_money.account_management_exception import AccountManagementException
from freezegun import freeze_time


class MyTestCase(unittest.TestCase):
    """Clase que contiene los tests de validación de transferencias bancarias (TC1 a TC23)."""

    @classmethod
    def setUpClass(cls):
        """Borra el archivo de transacciones antes de ejecutar todos los tests."""
        cls.manager = AccountManager()
        cls.test_file = cls.manager.transactions_file

        # Eliminar el archivo solo una vez al inicio
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

        # Eliminar el archivo si ya existe (para evitar duplicados)
        if os.path.exists(cls.test_file):
            os.remove(cls.test_file)

    #def tearDown(self):
    #    """Se ejecuta después de cada test: Borra el archivo JSON de pruebas."""
    #    if os.path.exists(self.test_file):
    #        os.remove(self.test_file)



    @freeze_time("2025-05-23")
    def test_valid_tc1(self):
        """Caso válido: Transferencia mínima"""
        result = self.manager.transfer_request(
            from_iban="ES9121000418450200051332",
            to_iban="ES6160606457126971492537",
            concept="Pago alquiler",
            transfer_type="ORDINARY",
            date="01/01/2027",
            amount=10.00
            )

        print(f"TC1 Hash: {result}")
        self.assertEqual(result, "60cf4031a7af271f0c5c3c4f1bb806d5")

        # Abrimos el archivo donde se guardó la transferencia
        with open(self.manager.transactions_file, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        # Buscamos si el código de transferencia está en el JSON
        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True

        # Afirmamos que se encontró
        self.assertTrue(found)


    @freeze_time("2025-05-23")
    def test_valid_tc2(self):
        """Caso válido: Transferencia con cantidad máxima"""
        result = self.manager.transfer_request(
            from_iban="ES9121000418450200051332",
            to_iban="ES6160606457126971492537",
            concept="Compra coche",
            transfer_type="URGENT",
            date="01/01/2027",
            amount=10000.00
        )
        print(f"TC2 Hash: {result}")
        self.assertEqual(result, "d5ec3dcc63cb81cd8eb416e57f494473")

        # Abrimos el archivo donde se guardó la transferencia
        with open(self.manager.transactions_file, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        # Buscamos si el código de transferencia está en el JSON
        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True

        # Afirmamos que se encontró
        self.assertTrue(found)

    @freeze_time("2025-05-23")
    def test_valid_tc3(self):
        """Caso válido: Transferencia con concepto largo"""
        result = self.manager.transfer_request(
            from_iban="ES9121000418450200051332",
            to_iban="ES6160606457126971492537",
            concept="Este es un concepto valido",
            transfer_type="INMEDIATE",
            date="01/01/2027",
            amount=10.01
        )
        print(f"TC3 Hash: {result}")
        self.assertEqual(result, "500e611f86d4ebbce180edb150106c9d")

        # Abrimos el archivo donde se guardó la transferencia
        with open(self.manager.transactions_file, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        # Buscamos si el código de transferencia está en el JSON
        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True

        # Afirmamos que se encontró
        self.assertTrue(found)

    @freeze_time("2025-05-23")
    def test_valid_tc4(self):
        """Caso válido: Transferencia al límite de la fecha permitida"""
        result = self.manager.transfer_request(
            from_iban="ES9121000418450200051332",
            to_iban="ES6160606457126971492537",
            concept="Pago seguro de la casa",
            transfer_type="ORDINARY",
            date="30/11/2050",
            amount=9999.99
        )
        print(f"TC4 Hash: {result}")
        self.assertEqual(result, "6c56a332a1b923d4effe6ad0dc51f23a")

        # Abrimos el archivo donde se guardó la transferencia
        with open(self.manager.transactions_file, "r", encoding="utf-8") as file:
            data_list = json.load(file)

        # Buscamos si el código de transferencia está en el JSON
        found = False
        for item in data_list:
            if item["transfer_code"] == result:
                found = True

        # Afirmamos que se encontró
        self.assertTrue(found)

    @freeze_time("2025-05-23")
    def test_not_valid_tc5(self):
        """TC5: IBAN inválido (no empieza por ES)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="DE1111111111111111111111",
                to_iban="DE1111111111111111111111",
                concept="1111111111",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=12
            )
        self.assertEqual(str(cm.exception), "ERROR from iban not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc6(self):
        """TC6: IBAN con caracteres incorrectos (demasiados dígitos)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES76 2085 9291 6400 1234 56800",
                to_iban="ES9121000418450200051332",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR from iban not valid")


    @freeze_time("2025-05-23")
    def test_not_valid_tc7(self):
        """TC7: Fecha inválida (día 32)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="32/01/2025",
                amount=100.00
            )
        self.assertEqual(str(cm.exception), "ERROR date not valid")


    @freeze_time("2025-05-23")
    def test_not_valid_tc8(self):
        """TC8: Cantidad superior al límite (10000.01)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=10000.01
            )
        self.assertEqual(str(cm.exception), "ERROR amount not valid")


    @freeze_time("2025-05-23")
    def test_not_valid_tc9(self):
        """TC9: Cantidad inferior al mínimo (9.99)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=9.99
            )
        self.assertEqual(str(cm.exception), "ERROR amount not valid")


    @freeze_time("2025-05-23")
    def test_not_valid_tc10(self):
        """TC10: Fecha malformada (mes 15)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="01/15/2025",  # MM=15
                amount=200.0
            )
        self.assertEqual(str(cm.exception), "ERROR date not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc11(self):
        """TC11: Fecha en el pasado"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="02/01/2024",  # fecha anterior al freeze_time
                amount=500.0
            )
        self.assertEqual(str(cm.exception), "ERROR date not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc12(self):
        """TC12: Fecha malformada (mes 13)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="01/13/2025",  # MM=13
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR date not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc13(self):
        """TC13: Fecha malformada (falta el día)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="01/2025",  # Formato incorrecto
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR date not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc14(self):
        """TC14: Fecha malformada con separadores incorrectos"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept",
                transfer_type="ORDINARY",
                date="01//01//2027",  # Formato con dobles barras
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR date not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc15(self):
        """TC15: Fecha con mes 0"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="concepto válido correcto",
                transfer_type="ORDINARY",
                date="01/00/2026",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR date not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc16(self):
        """TC16: Concepto muy corto"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="Hola",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR concept not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc17(self):
        """TC17: Tipo de transferencia no válido"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="correct concept value",
                transfer_type="EXPRESS",  # No válido
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR transfer type not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc18(self):
        """TC18: Concepto con una sola palabra"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="Alquiler",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR concept not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc19(self):
        """TC19: Concepto demasiado largo"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="Esto es un concepto extremadamente largo y fuera de límite",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR concept not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc20(self):
        """TC20: Concepto demasiado corto (menos de 10 caracteres)"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES6160606457126971492537",
                concept="Muycorto",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR concept not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc21(self):
        """TC21: IBAN de destino inválido"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="INVALIDO",
                concept="Pago correcto",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR to iban not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc22(self):
        """TC22: IBAN de destino con caracteres no numéricos"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES91ABCDE418450200051332",
                concept="Pago alquiler correcto",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR to iban not valid")

    @freeze_time("2025-05-23")
    def test_not_valid_tc23(self):
        """TC23: IBAN de destino con menos de 24 caracteres"""
        my_manager = AccountManager()
        with self.assertRaises(AccountManagementException) as cm:
            my_manager.transfer_request(
                from_iban="ES9121000418450200051332",
                to_iban="ES918450200051332",
                concept="Pago de préstamo correcto",
                transfer_type="ORDINARY",
                date="01/01/2027",
                amount=100.0
            )
        self.assertEqual(str(cm.exception), "ERROR to iban not valid")




if __name__ == '__main__':
    unittest.main()
