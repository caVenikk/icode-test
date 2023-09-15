class ContractNotFoundException(Exception):
    def __init__(self, contract_id):
        self.message = f"Договор с номером {contract_id} не найден"
        super().__init__(self.message)


class CannotSignCompletedContractException(Exception):
    def __init__(self, contract_id):
        self.message = f"Договор с номером {contract_id} уже завершен"
        super().__init__(self.message)
