import ctypes
import socket
from Modbus.ModbusRequest import ModbusRequest
from Modbus.ModbusResponse import ModbusResponse
from Modbus.WriteResponse import ModbusWriteResponse


class ModbusWriteRequest(ModbusRequest):
    def __init__(self, unit_id, function_code, register_address: ctypes.c_ushort, register_value: ctypes.c_ushort):
        super().__init__(unit_id, function_code)
        self.RegisterAddress = register_address
        self.RegisterValue = register_value

    def as_bytes(self) -> bytearray:
        message = super().as_bytes()
        message[8:10] = socket.htons(self.RegisterAddress).to_bytes(2, "little")
        message[10:12] = socket.htons(self.RegisterValue).to_bytes(2, "little")
        return message

    @classmethod
    def get_response_class(cls) -> type(ModbusResponse):
        return ModbusWriteResponse