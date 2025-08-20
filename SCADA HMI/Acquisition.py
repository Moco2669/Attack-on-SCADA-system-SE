import time
from threading import Thread
from threading import Event
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
            try:
                self.acquisition()
                self.automation()
            except Exception as error:
                print(f"Error during acquisition or automation: {error}")
                continue
            time.sleep(self.database.base_info["dbc"])
        print("Acquisition thread stopped.")

    def acquisition(self):
        read_requests = self.make_read_requests()
        requests_and_responses = self.process_requests(read_requests)
        self.database.update_registers_with(requests_and_responses)

    def automation_logic(self, control_rods_address, command, function_code=5):
        write_request = ModbusWriteRequest(self.database.base_info["station_address"], function_code,
                                               self.database.registers[control_rods_address].start_address,
                                               command)
        response = self.connection.request(write_request.as_bytes())
        modbus_response = ModbusWriteResponse.from_bytes(response)
        modbus_response.evaluate_with(write_request)
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

    def process_requests(self, requests: list[ModbusReadRequest]):
        responses_to_requests = dict()
        for read_request in requests:
            response = self.connection.request(read_request.as_bytes())
            modbus_response = ModbusReadResponse.from_bytes(response)
            modbus_response.evaluate_with(read_request)
            responses_to_requests[read_request] = modbus_response
        return responses_to_requests

    def make_read_requests(self) -> list[ModbusReadRequest]:
        unit_id = self.database.base_info["station_address"]
        list_of_requests = list()
        for register in self.database.registers_list:
            request = ModbusReadRequest(unit_id, register.read_function_code, register.start_address, register.num_reg)
            list_of_requests.append(request)
        return list_of_requests

    def wake_up(self):
        self.connected_event.set()
        self.connected_event.clear()

    def stop(self):
        self._running = False
        self.wake_up()
        self._program_loop.join()