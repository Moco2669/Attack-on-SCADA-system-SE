from Modbus.ModbusBase import ModbusBase
from Modbus.ModbusResponse import ModbusResponse


class ModbusWriteResponse(ModbusResponse):
    def __init__(self, unit_id, function_code, transaction_id, length, register_address, register_value):
        super().__init__(unit_id, function_code, transaction_id, length)
        self.RegisterAddress = register_address
        self.RegisterValue  = register_value

    @classmethod
    def from_bytes(cls, bytes_array: bytearray):
        transaction_id, length, unit_id, function_code = cls._create_base_from_bytes(bytes_array)
        register_address = int.from_bytes(bytes_array[8:10], byteorder="big", signed=False)
        register_value = int.from_bytes(bytes_array[10:12], byteorder="big", signed=False)

        instance = cls(
            unit_id = unit_id,
            function_code = function_code,
            transaction_id = transaction_id,
            length = length,
            register_address = register_address,
            register_value = register_value
        )

        return instance

    def evaluate_with(self, write_request: ModbusBase):
        super().evaluate_with(write_request)
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