import time
from SendReadRequest import *
from Modbus.ReadResponse import *
from AutomationManager import *
import Connection


class Executor:
    def __init__(self, database: DataBase):
        self.database = database

    def acquisition_and_automation(self):
        while Connection.ConnectionHandler.isRunning:
            read_requests = read_requests_from(self.database.base_info, self.database.registers_list)
            for read_request in read_requests:
                if Connection.ConnectionHandler.isConnected and Connection.ConnectionHandler.isRunning:
                    with Connection.ConnectionHandler.connection_lock:
                        try:
                            Connection.ConnectionHandler.client.send(read_request.as_bytes())
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
                    op = eOperation(response, read_request.FunctionCode)
                    if op == False:
                        modbus_response = ModbusReadResponse.from_bytes(response)
                        self.database.registers[read_request.StartAddress].current_value = modbus_response.get_data
            # ovde se pozivao log
            # dataForCSV(registers)
            automation(self.database.registers, self.database.base_info)
            time.sleep(1)
        print("Acquisition thread stopped.")
