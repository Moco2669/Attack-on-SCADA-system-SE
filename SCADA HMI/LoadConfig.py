from Modbus.Signal import *


def load_cfg(file_name):
    with open(file_name, 'r') as file:
        file_contents = file.readlines()
    base_info, signals = process(file_contents)
    return base_info, signals

def process(file_contents):
    base_info = process_headers(file_contents)
    signals = {}
    for row in file_contents[5:]:
        signal = process_registers(row)
        signals[signal.start_address] = signal
    return base_info, signals

def process_headers(file_contents):
    station_address = int(file_contents[0].split()[1])
    num_port = int(file_contents[1].split()[1])
    dbc = int(file_contents[3].split()[1])
    return {"station_address": station_address, "num_port": num_port, "dbc": dbc}

def process_registers(row):
    parameters = row.split()
    register_type = parameters[0]
    num_of_registers = int(parameters[1])
    address = int(parameters[2])
    min_value = int(parameters[3])
    max_value = int(parameters[4])
    start_value = int(parameters[5])
    signal_type = parameters[6]
    min_alarm = "NO ALARM" if not(parameters[7].isdigit()) else int(parameters[7])
    max_alarm = "NO ALARM" if not(parameters[8].isdigit()) else int(parameters[8])
    name = parameters[9].split(":")[1]
    return Signal(register_type, num_of_registers, address, min_value, max_value, start_value, signal_type, min_alarm, max_alarm, name)
