from GUI.TableRow import TableRow
from LoadConfig import *
from Modbus.ModbusRequest import ModbusRequest
from Modbus.ModbusResponse import ModbusResponse
from Modbus.ReadRequest import ModbusReadRequest
from Modbus.ReadResponse import ModbusReadResponse
from Modbus.WriteRequest import ModbusWriteRequest
from Modbus.WriteResponse import ModbusWriteResponse

"""
STA - adresa stanice -1 do 254 -> adresa scada sistema
Broj porta -> >1024 na kom je podignut(server/simulator)
DBC -> delay izmedju komandi
"""
"Ovde se cuvaju informacije o signalima "
"""
"Name", "Type", "Address", "Value", "Alarm"
"""


class DataBase:
    def __init__(self):
        self._event_handlers = {}
        self._app_running = True
        self._scada_connected = False
        self._base_info = None
        self._registers = None
        self._system_state = "NORMAL STATE"
        self.load_data('cfg.txt')

    @property
    def system_state(self):
        return self._system_state

    @property
    def app_running(self):
        return self._app_running

    @property
    def scada_connected(self):
        return self._scada_connected

    @scada_connected.setter
    def scada_connected(self, value: bool):
        self._scada_connected = value

    @system_state.setter
    def system_state(self, value: str):
        self._system_state = value

    @property
    def base_info(self):
        return self._base_info

    @property
    def registers(self):
        return self._registers

    @property
    def registers_list(self):
        return self._registers.values()

    def update_registers_with(self, modbus_pairs: dict[ModbusReadRequest, ModbusReadResponse]):
        for request in modbus_pairs.keys():
            self.registers[request.StartAddress].current_value = modbus_pairs[request].get_data

    def update_registers_with_write(self, modbus_pairs: dict[ModbusWriteRequest, ModbusWriteResponse]):
        for request in modbus_pairs.keys():
            self.registers[request.RegisterAddress].current_value = modbus_pairs[request].RegisterValue

    def load_data(self, file_name):
        self._base_info, self._registers = load_cfg(file_name)

    def scada_connected_notify(self):
        self._scada_connected = True
        self.emit("scada_connected")

    def stop(self):
        self.emit("stop")

    def event(self, event_name):
        def decorator(func):
            if event_name not in self._event_handlers:
                self._event_handlers[event_name] = []
            self._event_handlers[event_name].append(func)
            return func
        return decorator

    def emit(self, event_name, *args, **kwargs):
        if event_name in self._event_handlers:
            for handler in self._event_handlers[event_name]:
                handler(*args, **kwargs)

    def get_rows_for_print(self) -> list[TableRow]:
        row_list = list()
        for key, signal in self.registers.items():
            row_list.append(TableRow(signal))
        return row_list