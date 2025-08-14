from Modbus.ReadResponse import *
from Modbus.ReadRequest import *
from Modbus.Signal import *


def read_requests_from(base_info, registers : list[Signal]):
    unit_id = base_info["station_address"]
    list_of_request = list()
    for register in registers:
        request = ModbusReadRequest(unit_id, register.read_function_code, register.start_address, register.num_reg, )
        list_of_request.append(request.as_bytes())

    return list_of_request


def ResponseMessage(responseMessage) -> bytearray:
    base = ModbusBase(responseMessage[7], responseMessage[8])
    data = socket.ntohs(responseMessage[9:])
    return ModbusReadResponse(base, responseMessage[9], data)


def parseResponse(ModbusReadResponse: ModbusReadResponse, address, signals_info):
    signals_info[address].currentValue(ModbusReadResponse.Data)
