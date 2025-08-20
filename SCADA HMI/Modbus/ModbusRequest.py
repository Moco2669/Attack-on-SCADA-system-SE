import socket
from abc import ABC, abstractmethod
from Modbus.ModbusBase import ModbusBase
from Modbus.ModbusResponse import ModbusResponse


class ModbusRequest(ModbusBase, ABC):
    counter = 0
    def __init__(self, unit_id, function_code):
        super().__init__(unit_id, function_code)
        self.Length += 4
        self._increment_counter()
        self.TransactionID = self._get_counter_value()

    def as_bytes(self) -> bytearray:
        message = bytearray(12)
        message[0:2] = socket.htons(self.TransactionID).to_bytes(2, "little")
        message[2:4] = socket.htons(self.ProtocolID).to_bytes(2, "little")
        message[4:6] = socket.htons(self.Length).to_bytes(2, "little")
        message[6] = int(self.UnitID)
        message[7] = int(self.FunctionCode)
        return message

    @staticmethod
    def _increment_counter():
        ModbusRequest.counter += 1
        if ModbusRequest.counter == 65535:
            ModbusRequest.counter = 0

    @staticmethod
    def _get_counter_value() -> int:
        return ModbusRequest.counter

    @classmethod
    @abstractmethod
    def get_response_class(cls) -> type(ModbusResponse):
        pass