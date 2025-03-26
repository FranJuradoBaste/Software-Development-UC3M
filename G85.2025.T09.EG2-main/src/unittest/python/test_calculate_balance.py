"""Test para validar pruebas estructurales"""

# pylint: disable=too-many-public-methods

import unittest
import json
import os
from io import TextIOWrapper
from uc3m_money import AccountManager
from uc3m_money.account_management_exception import AccountManagementException
from freezegun import freeze_time



class MyTestCase(unittest.TestCase):
    """Test para validar pruebas estructurales"""

    def setUp(self):
        """Crea el archivo transactions2.json en la ruta correcta"""
        self.manager = AccountManager()

        # Ruta correcta hacia /src/JsonFiles
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self.json_folder = os.path.join(project_root, "JsonFiles")
        os.makedirs(self.json_folder, exist_ok=True)

        self.transactions_file = os.path.join(self.json_folder, "transactions2.json")
        self.balances_file = os.path.join(self.json_folder, "saldos.json")

        # Limpia archivos antes de cada test (opcional pero recomendado)
        for file in [self.transactions_file, self.balances_file]:
            if os.path.exists(file):
                os.remove(file)

    @freeze_time("2025-05-23")
    def test_calculate_balance_basic_path(self):
        """TC1: Prueba básica: el IBAN aparece una vez, suma correcta"""

        # Crear archivo transactions2.json con una entrada válida
        data = [
            {
                "IBAN": "ES9121000418450200051332",
                "amount": "+123.45"
            }
        ]
        with open(self.transactions_file, "w", encoding="utf-8") as f: # type: TextIOWrapper
            json.dump(data, f, indent=4)

        # Ejecutar la función
        result = self.manager.calculate_balance("ES9121000418450200051332")

        # Validar que devuelve True
        self.assertTrue(result)

    @freeze_time("2025-05-23")
    def test_calculate_balance_multiple_entries(self):
        """TC2: Varias entradas para el mismo IBAN, bucle ejecutado varias veces"""

        iban = "ES9121000418450200051332"
        transactions = [
            {"IBAN": iban, "amount": "+100.00"},
            {"IBAN": iban, "amount": "+200.50"},
            {"IBAN": iban, "amount": "-50.00"}
        ]
        with open(self.transactions_file, "w", encoding="utf-8") as f: # type: TextIOWrapper
            json.dump(transactions, f, indent=4)

        result = self.manager.calculate_balance(iban)
        self.assertTrue(result)

        # Verificar resultado acumulado en saldos.json
        with open(self.balances_file, "r", encoding="utf-8") as f:
            saldos = json.load(f)

        self.assertEqual(saldos[-1]["saldos"], 250.5)


    @freeze_time("2025-05-23")
    def test_calculate_balance_file_not_found(self):
        """TC3: El archivo de transacciones no existe"""

        if os.path.exists(self.transactions_file):
            os.remove(self.transactions_file)

        with self.assertRaises(AccountManagementException) as cm:
            self.manager.calculate_balance("ES9121000418450200051332")

        self.assertEqual(str(cm.exception), "ERROR file not found")

    @freeze_time("2025-05-23")
    def test_calculate_balance_iban_not_found(self):
        """TC4: El IBAN no aparece en transactions2.json"""

        data = [
            {"IBAN": "ES9999999999999999999999", "amount": "+50.00"},
            {"IBAN": "ES8888888888888888888888", "amount": "-25.00"}
        ]
        with open(self.transactions_file, "w", encoding="utf-8") as f: # type: TextIOWrapper
            json.dump(data, f, indent=4)

        with self.assertRaises(AccountManagementException) as cm:
            self.manager.calculate_balance("ES9121000418450200051332")

        self.assertEqual(str(cm.exception), "ERROR iban not found")

    @freeze_time("2025-05-23")
    def test_calculate_balance_invalid_json_format(self):
        """TC5: Formato JSON no válido"""

        with open(self.transactions_file, "w", encoding="utf-8") as f:
            f.write('{"IBAN": "ES9121000418450200051332", "amount": "+123.45"')  # Falta cierre

        with self.assertRaises(AccountManagementException) as cm:
            self.manager.calculate_balance("ES9121000418450200051332")

        self.assertEqual(str(cm.exception), "ERROR reading transaction file")



    @freeze_time("2025-05-23")
    def test_calculate_balance_invalid_iban(self):
        """TC6: El IBAN tiene un formato no válido"""

        data = [
            {"IBAN": "ES9999999999999999999999", "amount": "+100.00"}
        ]
        with open(self.transactions_file, "w", encoding="utf-8") as f: # type: TextIOWrapper
            json.dump(data, f, indent=4)

        # Ejecutamos con un IBAN incorrecto (formato no válido)
        with self.assertRaises(AccountManagementException) as cm:
            self.manager.calculate_balance("ES9999999999999999999999")

        # Comprobamos que se lanza el error correcto
        self.assertEqual(str(cm.exception), "ERROR iban not valid")

    @freeze_time("2025-05-23")
    def test_loop_executes_once(self):
        """TC7: El IBAN aparece solo una vez"""
        data = [
            {"IBAN": "ES9121000418450200051332", "amount": "+150.00"},
            {"IBAN": "ES0000000000000000000000", "amount": "+20.00"}
        ]
        with open(self.transactions_file, "w", encoding="utf-8") as f: # type: TextIOWrapper
            json.dump(data, f, indent=4)

        result = self.manager.calculate_balance("ES9121000418450200051332")
        self.assertTrue(result)

        with open(self.balances_file, "r", encoding="utf-8") as f:
            saldos = json.load(f)

        self.assertEqual(saldos[-1]["saldos"], 150.00)

    @freeze_time("2025-05-23")
    def test_loop_executes_multiple_times(self):
        """TC8: El IBAN aparece varias veces"""
        data = [
            {"IBAN": "ES9121000418450200051332", "amount": "+100.00"},
            {"IBAN": "ES9121000418450200051332", "amount": "+200.00"},
            {"IBAN": "ES9121000418450200051332", "amount": "-50.00"},
            {"IBAN": "ES0000000000000000000000", "amount": "+10.00"}
        ]
        with open(self.transactions_file, "w", encoding="utf-8") as f: # type: TextIOWrapper
            json.dump(data, f, indent=4)

        result = self.manager.calculate_balance("ES9121000418450200051332")
        self.assertTrue(result)

        with open(self.balances_file, "r", encoding="utf-8") as f:
            saldos = json.load(f)

        self.assertEqual(saldos[-1]["saldos"], 250.00)

    @freeze_time("2025-05-23")
    def test_loop_with_invalid_amounts(self):
        """TC9: Una entrada tiene amount inválido, se ignora"""
        data = [
            {"IBAN": "ES9121000418450200051332", "amount": "+100.00"},
            {"IBAN": "ES9121000418450200051332", "amount": "NO_ES_NUMERO"},
            {"IBAN": "ES9121000418450200051332", "amount": "+50.00"}
        ]
        with open(self.transactions_file, "w", encoding="utf-8") as f: # type: TextIOWrapper
            json.dump(data, f, indent=4)

        result = self.manager.calculate_balance("ES9121000418450200051332")
        self.assertTrue(result)

        with open(self.balances_file, "r", encoding="utf-8") as f:
            saldos = json.load(f)

        self.assertEqual(saldos[-1]["saldos"], 150.00)  # La segunda entrada es ignorada


if __name__ == '__main__':
    unittest.main()
