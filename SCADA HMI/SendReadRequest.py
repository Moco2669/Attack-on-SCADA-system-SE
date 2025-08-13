from Modbus.ReadResponse import *
from Modbus.ReadRequest import *
from Modbus.Signal import *


def read_requests_from(base_info, registers : list[Signal]):
    unit_id = base_info["station_address"]
    list_of_request = list()
    for register in registers:
        base = ModbusBase(unit_id, register.read_function_code)
        request = ModbusReadRequest(base, register.start_address, register.num_reg)
        list_of_request.append(repack(request))

    return list_of_request


def ResponseMessage(responseMessage) -> bytearray:
    base = ModbusBase(responseMessage[7], responseMessage[8])
    data = socket.ntohs(responseMessage[9:])
    return ModbusReadReasponse(base, responseMessage[9], data)


def parseResponse(ModbusReadResponse: ModbusReadReasponse, address, signals_info):
    signals_info[address].currentValue(ModbusReadResponse.Data)
