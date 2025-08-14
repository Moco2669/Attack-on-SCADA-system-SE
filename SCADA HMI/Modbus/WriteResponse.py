from Modbus.ModbusBase import *
import ctypes
"""
Klasa je samo kako bi se razlikovali Request Write i Response za Write sustinski su isti objekti
"""
class ModbusWriteResponse(ModbusBase):
    def __init__(self, unit_id, function_code,
                 register_address : ctypes.c_ushort,
                 register_value : ctypes.c_ushort):
        super().__init__(unit_id, function_code)
        self.RegisterAddress = register_address
        self.RegisterValue  = register_value

    @classmethod
    def from_bytes(cls, bytes_array: bytearray):
        transaction_id = int.from_bytes(bytes_array[0:2],byteorder="big",signed=False)
        length = int.from_bytes(bytes_array[4:6], byteorder="big", signed=False)
        unit_id = int.from_bytes(bytes_array[6:7], byteorder="big", signed=False)
        function_code = int.from_bytes(bytes_array[7:8], byteorder="big", signed=False)
        register_address = int.from_bytes(bytes_array[8:10], byteorder="big", signed=False)
        register_value = int.from_bytes(bytes_array[10:12], byteorder="big", signed=False)

        instance = cls(
            unit_id = unit_id,
            function_code = function_code,
            register_address = register_address,
            register_value= register_value
        )

        instance.TransactionID = transaction_id
        instance.Length = length

        return instance

    def __str__(self):
        return f"{super().__str__()},RegisterAdress:{self.RegisterAddress},RegisterValue:{self.RegisterValue}"

    def getFunctionCode(self):
        return self.FunctionCode
