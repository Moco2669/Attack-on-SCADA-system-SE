from Modbus.ModbusBase import *
import ctypes


class ModbusReadResponse(ModbusBase):
    def __init__(self, unit_id, function_code, byte_count : ctypes.c_byte, data : bytearray):
        super().__init__(unit_id, function_code)
        self.ByteCount = byte_count
        self.Data = data

    @classmethod
    def from_bytes(cls, bytes_array: bytearray):
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


    @property
    def get_data(self):
        return self.Data


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
