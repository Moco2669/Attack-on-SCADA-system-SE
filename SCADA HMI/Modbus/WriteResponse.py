from Modbus.ModbusBase import *
import ctypes

from Modbus.WriteRequest import ModbusWriteRequest

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

    def evaluate_with(self, write_request: ModbusWriteRequest):
        if not self.TransactionID == write_request.TransactionID:
            raise ValueError("Transaction ID mismatch in response evaluation")
        if not self.ProtocolID == write_request.ProtocolID:
            raise ValueError("Protocol ID mismatch in response evaluation")
        if not self.UnitID == write_request.UnitID:
            raise ValueError("Unit ID mismatch in response evaluation")
        if int(self.FunctionCode) == int(write_request.FunctionCode) + 128:
            match self.RegisterValue:
                case 1:
                    raise ValueError("Exception in response: Illegal function")
                case 2:
                    raise ValueError("Exception in response: Illegal data address")
                case 3:
                    raise ValueError("Exception in response: Illegal data value")
        if not self.FunctionCode == write_request.FunctionCode:
            raise ValueError("Function code mismatch in response evaluation")
        if not self.RegisterAddress == write_request.RegisterAddress:
            raise ValueError("Register address mismatch in response evaluation")
        if not self.RegisterValue == write_request.RegisterValue:
            raise ValueError("Register value mismatch in response evaluation")
        if not self.Length == write_request.Length:
            raise ValueError("Length mismatch in response evaluation")