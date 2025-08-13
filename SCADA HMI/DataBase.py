from GUI.TableRow import TableRow
from LoadConfig import *
from Modbus.Signal import *
"""
STA - adresa stanice -1 do 254 -> adresa scada sistema
Broj porta -> >1024 na kom je podignut(server/simulator)
DBC -> delay izmedju komandi
"""
base_info = {}
"Ovde se cuvaju informacije o signalima "
signal_info = {}
base_info, signal_info = load_cfg('cfg.txt')
"""
"Name", "Type", "Address", "Value", "Alarm"
"""


def get_rows_for_print(signal_info):
    row_list = list()
    for key, signal in signal_info.items():
        row_list.append(TableRow(signal))
    return row_list


class DataBase:
    def __init__(self):
        self.base_info = None
        self.signal_info = None

    def load_data(self, file_name):
        self.base_info, self.signal_info = load_cfg(file_name)