import socket

from Modbus.ModbusBase import *
import ctypes
"""
Objekat koji ce primati read odgovore 
"""

class ModbusReadResponse(ModbusBase):
    def __init__(self, unit_id, function_code, byte_count : ctypes.c_byte, data : bytearray):
        super().__init__(unit_id, function_code)
        self.ByteCount = byte_count
        self.Data = data

    @classmethod
    def from_bytes(cls, bytes_array: bytearray):
        """super().__init__(int.from_bytes(bytes_array[6:7], byteorder="big", signed=False), int.from_bytes(bytes_array[7:8], byteorder="big", signed=False))
        cls.ByteCount = int.from_bytes(bytes_array[8:9], byteorder="big", signed=False)
        cls.Data = int.from_bytes(bytes_array[9:], byteorder="big", signed=False)
        cls.TransactionID = int.from_bytes(bytes_array[0:2], byteorder="big", signed=False)
        cls.Length = int.from_bytes(bytes_array[4:6], byteorder="big", signed=False)"""
        transaction_id = int.from_bytes(bytes_array[0:2], byteorder="big", signed=False)
        length = int.from_bytes(bytes_array[4:6], byteorder="big", signed=False)
        unit_id = int.from_bytes(bytes_array[6:7], byteorder="big", signed=False)
        function_code = int.from_bytes(bytes_array[7:8], byteorder="big", signed=False)
        byte_count = int.from_bytes(bytes_array[8:9], byteorder="big", signed=False)
        data = int.from_bytes(bytes_array[9:], byteorder="big", signed=False)

        instance = cls(
            unit_id = unit_id,
            function_code = function_code,
            byte_count = byte_count,
            data = data
        )

        instance.TransactionID = transaction_id
        instance.Length = length

        return instance


    def __str__(self):
        return f"{super().__str__()},ByteCount:{self.ByteCount},Data:{self.Data}"

    def get_data(self):
        return self.Data

    def setTransactionID(self, value):
        self.TransactionID = value


    def setProtocolID(self, value):
        self.ProtocolID = value


    def setLength(self, value):
        self.Length = value


    def setUnitID(self, value):
        self.UnitID = value

    def setFunctionCode(self, value):
        self.FunctionCode = value

"""
Summary how to repack this message from scada sim 

1. ushort transactionID 
2. ushort protocolID 
3. ushort length 
4. byte unit id 
5. byte function code 
6. byte byteCount 
7. n-bytes data  
"""
