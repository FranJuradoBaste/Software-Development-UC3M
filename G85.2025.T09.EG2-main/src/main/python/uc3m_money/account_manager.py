"""Módulo account_manager: gestiona transferencias y validaciones bancarias."""


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
from io import TextIOWrapper
import json
import os
import hashlib
from datetime import datetime, UTC
from datetime import timezone
from uc3m_money.account_management_exception import AccountManagementException
from uc3m_money.transfer_request import TransferRequest




class AccountManager:
    """Class for managing account transactions"""

    def __init__(self):
        """Define the JSON file to store transactions"""
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        # Ruta a la carpeta JsonFiles dentro de /src
        json_folder = os.path.join(project_root, "JsonFiles")
        os.makedirs(json_folder, exist_ok=True)
        self.transactions_file = os.path.join(json_folder, "transactions.json")

    @staticmethod
    def validate_iban(iban):
        """Valida que sea un str"""
        if not isinstance(iban, str):
            return False

        # Valida las mayúsculas y quita los espacios
        iban = iban.replace(" ", "").upper()

        # Valida que comienza con ES
        if not iban.startswith("ES"):
            return False

        # Valida la longitud del IBAN
        if len(iban) != 24:
            return False

        # Validacion de que los dígitos luego de ES
        if not iban[2:].isdigit():
            return False

        rearranged_iban = iban[4:] + iban[:4]

        numeric_iban = []
        for ch in rearranged_iban:
            if ch.isdigit():
                numeric_iban.append(str(ch))  # Mantiene los números iguales
            else:
                numeric_iban.append(str(ord(ch) - 55))  # Convierte letras

        numeric_iban = ''.join(numeric_iban)

        return int(numeric_iban) % 97 == 1

    def transfer_request(self,
                         from_iban: str,
                         to_iban: str,
                         concept: str,
                         transfer_type: str,
                         date: str,
                         amount: float):
        """ Verifica los datos de la solicitud de transferencia y la registra en un archivo JSON """
        if not self.validate_iban(from_iban):
            raise AccountManagementException("ERROR from iban not valid")
        if not self.validate_iban(to_iban):
            raise AccountManagementException("ERROR to iban not valid")
        if not (10 <= len(concept) <= 30 and len(concept.split()) >= 2):
            raise AccountManagementException("ERROR concept not valid")
        if transfer_type not in {"ORDINARY", "URGENT", "INMEDIATE"}:
            raise AccountManagementException("ERROR transfer type not valid")
        try:
            transfer_date = datetime.strptime(date, "%d/%m/%Y")
            today = datetime.today()
            if not (2025 <= transfer_date.year < 2051 and transfer_date >= today):
                raise AccountManagementException("ERROR date not valid")
        except ValueError as exc:
            raise AccountManagementException("ERROR date not valid") from exc
        if not (10.00 <= amount <= 10000.00 and len(str(amount).split(".")) <= 2):
            raise AccountManagementException("ERROR amount not valid")
        transfer = TransferRequest(from_iban, transfer_type, to_iban, concept, date, amount)
        transfer_code = transfer.transfer_code

        transfer_data = transfer.to_json()

        # Guardar en JSON
        if os.path.exists(self.transactions_file):
            with open(self.transactions_file, "r", encoding="utf-8") as file:
                try:
                    transactions = json.load(file)
                except json.JSONDecodeError:
                    transactions = []
        else:
            transactions = []

        if transfer_data in transactions:
            raise AccountManagementException("ERROR transfer already exists")

        transactions.append(transfer_data)
        with open(self.transactions_file, "w", encoding="utf-8") as file:  # type: TextIOWrapper
            json.dump(transactions, file, indent=4)

        return transfer_code


    def deposit_into_account(self, input_file: str) -> str:
        """
        Procesa un ingreso a cuenta desde un archivo JSON.
        Devuelve la firma (SHA-256) del ingreso o lanza AccountManagementException.
        """

        if not os.path.exists(input_file):
            raise AccountManagementException("ERROR input file not found")
        try:
            with open(input_file, "r", encoding="utf-8") as file:
                data = json.load(file)

        except json.JSONDecodeError as exc:
            raise AccountManagementException("ERROR invalid JSON format") from exc
        except Exception as exc:
            raise AccountManagementException("ERROR reading input file") from exc

        if "IBAN" not in data or "AMOUNT" not in data:
            raise AccountManagementException("ERROR invalid input structure")

        iban = data["IBAN"]
        amount_str = data["AMOUNT"]

        if not self.validate_iban(iban):
            raise AccountManagementException("ERROR IBAN not valid")

        if not amount_str.startswith("EUR "):
            raise AccountManagementException("ERROR amount format invalid")

        amount = float(amount_str[4:])

        deposit_date = datetime.now(UTC).timestamp()

        deposit_dict = {
            "alg": "SHA-256",
            "typ": "DEPOSIT",
            "iban": iban,
            "amount": f"{amount:.2f}",
            "deposit_date": deposit_date
        }

        deposit_str = (
            f"{{alg:{deposit_dict['alg']},typ:{deposit_dict['typ']},"
            f"iban:{deposit_dict['iban']},amount:{deposit_dict['amount']},"
            f"deposit_date:{deposit_dict['deposit_date']}}}"
        )

        signature = hashlib.sha256(deposit_str.encode()).hexdigest()

        deposit_dict["deposit_signature"] = signature

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        deposits_path = os.path.join(project_root, "JsonFiles", "deposits.json")

        if os.path.exists(deposits_path):
            with open(deposits_path, "r", encoding="utf-8") as f:
                deposits = json.load(f)

        else:
            deposits = []
        deposits.append(deposit_dict)

        with open(deposits_path, "w", encoding="utf-8") as file:  # type: TextIOWrapper
            json.dump(deposits, file, indent=4)

        return signature

    def calculate_balance(self, iban_number: str) -> bool:
        """
        Calcula el saldo total de un IBAN a partir del archivo transactions2.json.
        Guarda o actualiza el resultado en saldos.json acumulando el saldo anterior.
        """
        if not self.validate_iban(iban_number):
            raise AccountManagementException("ERROR iban not valid")

        # Ruta a JSON
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
        json_folder = os.path.join(project_root, "JsonFiles")
        transactions_path = os.path.join(json_folder, "transactions2.json")

        if not os.path.exists(transactions_path):
            raise AccountManagementException("ERROR file not found")

        try:
            with open(transactions_path, "r", encoding="utf-8") as file:
                transactions = json.load(file)
        except Exception as exc:
            raise AccountManagementException("ERROR reading transaction file") from exc

        # Buscar y sumar movimientos del IBAN
        amounts = []
        for entry in transactions:
            if entry.get("IBAN") == iban_number:
                try:
                    amounts.append(float(entry.get("amount")))
                except (ValueError, TypeError):
                    continue

        if not amounts:
            raise AccountManagementException("ERROR iban not found")

        total_balance = sum(amounts)
        timestamp = datetime.now(timezone.utc).timestamp()

        # Guardar en saldos.json acumulando el saldo
        balances_path = os.path.join(json_folder, "saldos.json")
        if os.path.exists(balances_path):
            try:
                with open(balances_path, "r", encoding="utf-8") as file:
                    balances = json.load(file)
            except json.JSONDecodeError:
                balances = []
        else:
            balances = []

        # Buscar si ya existe una entrada para ese IBAN
        iban_found = False
        for entry in balances:
            if entry.get("iban") == iban_number:
                # Acumular el nuevo saldo
                entry["saldos"] = round(entry.get("saldos", 0.0) + total_balance, 2)
                entry["timestamp"] = timestamp
                iban_found = True
                break

        # Si no estaba, lo añadimos como nuevo
        if not iban_found:
            balances.append({
                "iban": iban_number,
                "saldos": round(total_balance, 2),
                "timestamp": timestamp
            })

        # Guardar de vuelta
        with open(balances_path, "w", encoding="utf-8") as f: # type: TextIOWrapper
            json.dump(balances, f, indent=4)

        return True
