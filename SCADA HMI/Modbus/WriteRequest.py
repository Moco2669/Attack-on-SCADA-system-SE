from Modbus.ModbusBase import *
import ctypes
import socket
"""Objekat koji se salje da bi se upisalo nesto
    RegisterAddress - > adresa registra na koji se upisuje vrednost 
    RegisterValue - > vrednost koja se upisuje u taj registar 
    Akko se uspesno izvrsi upravljanje u WriteResponse ce doci povratna poruka koja je ista kao poslata(WriteRequest)
"""


class ModbusWriteRequest(ModbusBase):
    value = 0
    def __init__(self, unit_id, function_code, register_address: ctypes.c_ushort, register_value: ctypes.c_ushort):
        super().__init__(unit_id, function_code)
        ModbusWriteRequest.value +=1
        if ModbusWriteRequest.value == 65535:
            ModbusWriteRequest.value = 0
        self.Length += 4 # zato sto je su registerAddres && register value fiksno 4 bajta
        self.TransactionID = ModbusWriteRequest.value
        self.RegisterAddress = register_address
        self.RegisterValue = register_value

    def as_bytes(self) -> bytearray:
        message = bytearray(12)
        message[0:2] = socket.htons(self.TransactionID).to_bytes(2, "little")
        message[2:4] = socket.htons(self.ProtocolID).to_bytes(2, "little")
        message[4:6] = socket.htons(self.Length).to_bytes(2, "little")
        message[6] = self.UnitID
        message[7] = self.FunctionCode
        message[8:10] = socket.htons(self.RegisterAddress).to_bytes(2, "little")
        message[10:12] = socket.htons(self.RegisterValue).to_bytes(2, "little")
        return message
