import time
from threading import Thread
from threading import Event
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
        requests_and_responses = self.process_read_requests(read_requests)
        self.database.update_registers_with(requests_and_responses)

    def automation_logic(self):
        list_of_requests = list()
        water_thermometer_address = 2000
        control_rods_address = 1000
        water_thermometer = self.database.registers[water_thermometer_address]
        control_rods = self.database.registers[control_rods_address]
        if water_thermometer.alarm == "HIGH ALARM":
            desired_value = 0xFF00
        elif water_thermometer.alarm == "LOW ALARM":
            desired_value = 0x0000
        else: return list_of_requests
        unit_id = self.database.base_info["station_address"]
        write_request = ModbusWriteRequest(unit_id, control_rods.write_function_code,
                                               control_rods.start_address, desired_value)
        list_of_requests.append(write_request)
        return list_of_requests

    def automation(self):
        write_requests = self.automation_logic()
        if len(write_requests) == 0: return
        requests_and_responses = self.process_write_requests(write_requests)
        self.database.registers[write_requests[0].RegisterAddress].current_value = write_requests[0].RegisterValue

    def process_read_requests(self, requests: list[ModbusReadRequest]):
        responses_to_requests = dict()
        for read_request in requests:
            response = self.connection.request(read_request.as_bytes())
            modbus_response = ModbusReadResponse.from_bytes(response)
            modbus_response.evaluate_with(read_request)
            responses_to_requests[read_request] = modbus_response
        return responses_to_requests

    def process_write_requests(self, requests: list[ModbusWriteRequest]):
        responses_to_requests = dict()
        for write_request in requests:
            response = self.connection.request(write_request.as_bytes())
            modbus_response = ModbusWriteResponse.from_bytes(response)
            modbus_response.evaluate_with(write_request)
            responses_to_requests[write_request] = modbus_response
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