import ctypes
import socket
from Modbus.ModbusRequest import ModbusRequest
from Modbus.ModbusResponse import ModbusResponse
from Modbus.ReadResponse import ModbusReadResponse


class ModbusReadRequest(ModbusRequest):
    def __init__(self, unit_id, function_code, start_address: ctypes.c_ushort, quantity: ctypes.c_ushort):
        super().__init__(unit_id, function_code)
        self.StartAddress = start_address
        self.Quantity = quantity

    def as_bytes(self) -> bytearray:
        request = super().as_bytes()
        request[8:10] = socket.htons(self.StartAddress).to_bytes(2, "little")
        request[10:12] = socket.htons(self.Quantity).to_bytes(2, "little")
        return request

    @classmethod
    def get_response_class(cls) -> type(ModbusResponse):
        return ModbusReadResponse
