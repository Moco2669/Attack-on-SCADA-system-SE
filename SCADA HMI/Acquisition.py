import time
from threading import Thread
from threading import Event
from SendReadRequest import *
from Modbus.ReadResponse import *
from AutomationManager import *
from Connection import ConnectionHandler


class Executor:
    def __init__(self, database: DataBase, connection: ConnectionHandler):
        self.connection = connection
        self.database = database
        self._running = True
        self.connected_event = Event()
        self._program_loop = Thread(target=self.acquisition_and_automation)
        self._program_loop.start()
        self.setup_handlers()

    def setup_handlers(self):
        @self.database.event("stop")
        def handle_stop():
            self.stop()

        @self.database.event("scada_connected")
        def handle_scada_connected():
            self.wake_up()

    def acquisition_and_automation(self):
        while self._running:
            if not self.database.scada_connected:
                self.connected_event.wait()
            self.acquisition()
            self.automation()
            time.sleep(1)
        print("Acquisition thread stopped.")

    def acquisition(self):
        read_requests = read_requests_from(self.database.base_info, self.database.registers_list)
        for read_request in read_requests:
            response = self.connection.request(read_request.as_bytes())
            if not response:
                continue
            op = eOperation(response, read_request.FunctionCode)
            if op == False:
                modbus_response = ModbusReadResponse.from_bytes(response)
                self.database.registers[read_request.StartAddress].current_value = modbus_response.get_data

    def automation_logic(self, control_rods_address, command, function_code=5):
        write_request = ModbusWriteRequest(self.database.base_info["station_address"], function_code,
                                               self.database.registers[control_rods_address].start_address,
                                               command)
        response = self.connection.request(write_request.as_bytes())
        if not response: return
        op = eOperation(response, function_code)
        if op == False:
            modbus_write_response = ModbusWriteResponse.from_bytes(response)
            if compare(write_request, modbus_write_response):
                self.database.registers[control_rods_address].current_value = command
    """
    Vrsi se provera alarma i desava se logika automatizacije 
    """

    def automation(self):
        water_thermometer_address = 2000  # pravi ovo da cita iz signal info
        control_rods_address = 1000
        if isHighAlarmActive(water_thermometer_address, self.database.registers):
            self.automation_logic(control_rods_address, 65280)  # #0xFF00 za 1
        elif isLowAlarmActive(water_thermometer_address, self.database.registers):
            self.automation_logic(control_rods_address, 0)

    def wake_up(self):
        self.connected_event.set()
        self.connected_event.clear()

    def stop(self):
        self._running = False
        self.wake_up()
        self._program_loop.join()