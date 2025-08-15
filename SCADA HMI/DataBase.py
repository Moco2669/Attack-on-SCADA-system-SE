from GUI.TableRow import TableRow
from LoadConfig import *
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
        self._app_running = True
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

    def load_data(self, file_name):
        self._base_info, self._registers = load_cfg(file_name)

    def stop(self):
        self._app_running = False

    def get_rows_for_print(self) -> list[TableRow]:
        row_list = list()
        for key, signal in self.registers.items():
            row_list.append(TableRow(signal))
        return row_list