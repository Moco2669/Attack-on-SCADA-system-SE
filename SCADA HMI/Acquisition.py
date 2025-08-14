import time as t
from SendReadRequest import *
from Modbus.ReadResponse import *
from AutomationManager import *
import Connection


class Executor:
    def __init__(self, database: DataBase):
        self.database = database

    def AcquisitionAndAutomation(self):
        while Connection.ConnectionHandler.isRunning:
            pack_request = read_requests_from(self.database.base_info, self.database.registers_list)
            for message in pack_request:
                if Connection.ConnectionHandler.isConnected and Connection.ConnectionHandler.isRunning:
                    with Connection.ConnectionHandler.connection_lock:
                        try:
                            Connection.ConnectionHandler.client.send(message)
                            response = Connection.ConnectionHandler.client.recv(1024)
                        except:
                            Connection.ConnectionHandler.isConnected = False
                            if not Connection.ConnectionHandler.isRunning:
                                break
                            Connection.ConnectionHandler.lostConnection.notify_all()
                            if not Connection.ConnectionHandler.isRunning:
                                break
                            Connection.ConnectionHandler.connected.wait()
                            continue
                    address = find_address(message)
                    functionCode = find_function_code(message)
                    op = eOperation(response, functionCode)
                    if op == False:
                        modbusresponse = ModbusReadResponse.from_bytes(response)
                        self.database.registers[address].current_value = modbusresponse.get_data()
            # ovde se pozivao log
            # dataForCSV(registers)
            Automation(self.database.registers, self.database.base_info)
            t.sleep(1)
        print("Acquisition thread stopped.")


class StateHolder(object):
    state = "NORMAL STATE"


def find_address(request):
    address = int.from_bytes(request[8:10], byteorder="big", signed=False)
    return address

def find_function_code(message):
    return int.from_bytes(message[7:8], byteorder="big", signed=False)

"""
Korisceno kako bi se skupljali podaci za treniranje 
"""
def dataForCSV(signal_info : dict):
    global counter
    global controlRodsList
    global waterThermometerList
    if counter != 3:
        for key,value in signal_info.items():
            match signal_info[key].signal_type:
                case "DO":
                    controlRodsList.append(signal_info[key].current_value())
                case "AI":
                    waterThermometerList.append(signal_info[key].current_value())
        counter+=1
    else:
        counter = 0
        # Read existing CSV file if it exists
        try:
            df = pd.read_csv('learningDataNew.csv')
        except FileNotFoundError:
            # If the file doesn't exist, create a new DataFrame with the updated header
            columns = [
                'WT_VALUE01', 'WT_VALUE02', 'WT_VALUE03',
                'CR_VALUE01', 'CR_VALUE02', 'CR_VALUE03',
                'REPLAY_ATTACK', 'COMMAND_INJECTION', 'NORMAL_STATE'
            ]
            df = pd.DataFrame(columns=columns)

        new_row = {
            'WT_VALUE01': int(waterThermometerList[0]),
            'WT_VALUE02': int(waterThermometerList[1]),
            'WT_VALUE03': int(waterThermometerList[2]),
            'CR_VALUE01': int(controlRodsList[0]),
            'CR_VALUE02': int(controlRodsList[1]),
            'CR_VALUE03': int(controlRodsList[2]),
            'REPLAY_ATTACK': 0,  # Replace with the actual values
            'COMMAND_INJECTION': 0,  # Replace with the actual values
            'NORMAL_STATE': 1  # Replace with the actual values
        }

        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        # Convert relevant columns to integers
        int_columns = ['WT_VALUE01', 'WT_VALUE02', 'WT_VALUE03','CR_VALUE01', 'CR_VALUE02', 'CR_VALUE03']
        df[int_columns] = df[int_columns].astype(int)

        # Write the updated DataFrame back to the CSV file
        df.to_csv('learningDataNew.csv', index=False)

        controlRodsList.clear()
        waterThermometerList.clear()
