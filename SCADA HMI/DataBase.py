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


def makeTuplesForPrint(signal_info):
    tuple_list = list()
    for key, value in signal_info.items():
        name = value._Name
        type = value._SignalType
        match value._SignalType:
            case "DO":
                type = "Digital Output"
            case "DI":
                type = "Digital Input"
            case "AO":
                type = "Analog Output"
            case "AI":
                type = "Analog Input"
            # mora ovako zato sto nece da ispisuje nesto sto nije int qt
        address = str(value._StartAddress)
        pocetna = str(value.current_value)
        alarm = value.alarm
        tuple_list.append((name,type,address,pocetna,alarm))
    return tuple_list
