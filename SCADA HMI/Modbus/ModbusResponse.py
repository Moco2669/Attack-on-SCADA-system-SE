from abc import ABC, abstractmethod
from Modbus.ModbusBase import ModbusBase


class ModbusResponse(ModbusBase, ABC):
    def __init__(self, unit_id, function_code, transaction_id, length):
        super().__init__(unit_id, function_code)
        self.TransactionID = transaction_id
        self.Length = length

    @classmethod
    def _create_base_from_bytes(cls, bytes_array: bytearray):
        transaction_id = int.from_bytes(bytes_array[0:2], byteorder="big", signed=False)
        length = int.from_bytes(bytes_array[4:6], byteorder="big", signed=False)
        unit_id = int.from_bytes(bytes_array[6:7], byteorder="big", signed=False)
        function_code = int.from_bytes(bytes_array[7:8], byteorder="big", signed=False)

        return transaction_id, length, unit_id, function_code

    @classmethod
    @abstractmethod
    def from_bytes(cls, bytes_array: bytearray):
        pass

    def evaluate_with(self, request: ModbusBase):
        if not self.TransactionID == request.TransactionID:
            raise ValueError("Transaction ID mismatch in response evaluation")
        if not self.ProtocolID == request.ProtocolID:
            raise ValueError("Protocol ID mismatch in response evaluation")
        if not self.UnitID == request.UnitID:
            raise ValueError("Unit ID mismatch in response evaluation")