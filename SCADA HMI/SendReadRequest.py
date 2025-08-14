from Modbus.ReadRequest import *
from Modbus.Signal import *


def read_requests_from(base_info, registers : list[Signal]) -> list[ModbusReadRequest]:
    unit_id = base_info["station_address"]
    list_of_request = list()
    for register in registers:
        request = ModbusReadRequest(unit_id, register.read_function_code, register.start_address, register.num_reg)
        list_of_request.append(request)
    return list_of_request
