import ctypes
from abc import ABC


class ModbusBase(ABC):
    def __init__(self, unit_id: ctypes.c_byte, function_code: ctypes.c_byte):
        self.TransactionID = 0 #ushort
        self.ProtocolID = 0 #ushort
        self.Length = 2 #ushort
        self.UnitID = unit_id
        self.FunctionCode = function_code
