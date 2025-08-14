from Modbus.ModbusBase import *
import ctypes
import socket

"""
startAdress - > sa koje adrese zeli da se procita 
quantity - > sa koliko uzastopnih registara treba da cita 
Primer: start adress 1000 
        quantity 2 
        => citace sa adrese 1000 i 1001 na svakoj adresi je 16bit registar 
"""


class ModbusReadRequest(ModbusBase):
    value = 0
    def __init__(self, unit_id, function_code, start_address: ctypes.c_ushort, quantity: ctypes.c_ushort):
        super().__init__(unit_id, function_code)
        ModbusReadRequest.value += 1
        self.TransactionID = ModbusReadRequest.value
        if ModbusReadRequest.value == 65535:
            ModbusReadRequest.value = 0
        self.Length += 4 # Start address and quantity is always 4 bytes
        self.StartAddress = start_address
        self.Quantity = quantity

    def as_bytes(self) -> bytearray:
        request = bytearray(12)
        request[0:2] = socket.htons(self.TransactionID).to_bytes(2, "little")
        request[2:4] = socket.htons(self.ProtocolID).to_bytes(2, "little")
        request[4:6] = socket.htons(self.Length).to_bytes(2, "little")
        request[6] = int(self.UnitID)
        request[7] = int(self.FunctionCode)
        request[8:10] = socket.htons(self.StartAddress).to_bytes(2, "little")
        request[10:12] = socket.htons(self.Quantity).to_bytes(2, "little")
        return request


