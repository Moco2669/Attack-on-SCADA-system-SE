import ctypes
from Modbus.ModbusBase import ModbusBase
from Modbus.ModbusResponse import ModbusResponse


class ModbusReadResponse(ModbusResponse):
    def __init__(self, unit_id, function_code, transaction_id, length, byte_count : ctypes.c_byte, data : bytearray):
        super().__init__(unit_id, function_code, transaction_id, length)
        self.ByteCount = byte_count
        self.Data = data

    @classmethod
    def from_bytes(cls, bytes_array: bytearray):
        transaction_id, length, unit_id, function_code = cls._create_base_from_bytes(bytes_array)
        byte_count = int.from_bytes(bytes_array[8:9], byteorder="big", signed=False)
        data = int.from_bytes(bytes_array[9:], byteorder="big", signed=False)

        instance = cls(
            unit_id = unit_id,
            function_code = function_code,
            transaction_id = transaction_id,
            length = length,
            byte_count = byte_count,
            data = data
        )

        return instance


    @property
    def get_data(self):
        return self.Data

    def evaluate_with(self, read_request : ModbusBase):
        super().evaluate_with(read_request)
        if int(self.FunctionCode) == int(read_request.FunctionCode) + 128:
            match self.ByteCount:
                case 1:
                    raise ValueError("Exception in response: Illegal function")
                case 2:
                    raise ValueError("Exception in response: Illegal data address")
                case 3:
                    raise ValueError("Exception in response: Illegal data value")

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
