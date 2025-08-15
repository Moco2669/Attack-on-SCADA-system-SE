"""
Ideja
Napisati metodu koja ce vrsiti konstantnu kontrolu pristiglih prednosti i na osnovu toga govoriti kakvo je stanje sistema,da li treba da se upali alarm
Kad se upali alarm treba da se reaguje(npr treba da se iskljuci prekidac neki)
Ako je sistem u neispravnom stanju i istom loopu poslati write poruku za gasenjem nekog prekidaca npr...
Prima se odgovor ako je uspesno izvrsena komanda i onda se se krece sa sledecim loopom i akvizicijom
Naravno ovo sve raditi samo za digitalnim i analognim izlazima --> nad izlaznim signalima se upravlja
Dok ulazni signali --> daju izlazne informacije o sistemu
"""
from DataBase import *
from typing import Dict
from Modbus.Signal import *
from Modbus.WriteRequest import *
from Modbus.WriteResponse import *
from Modbus.ModbusBase import *
import Connection

"""
Trazi addresu od control rods-a 
U slucaju da se promeni adresa iz configa 
"""


def takeControlRodsAddress(signal_info):
    for key, value in signal_info.items():
      if value[key].signal_type == "DO":
          return key


"""
Trazi addresu od water thermometer 
U slucaju da se promeni adresa iz configa 
"""


def takeWaterThermometerAddress(signal_info):
    for key,value in signal_info.items():
        if value[key].signal_type == "AI":
            return key


"""
F-ja koja se koristi da bi znali da li je uspesno izvrsen poslati write 
if writeRequest == writeResponse -> uspesno izvrseno 
else nije izvrseno 
"""


def compare(write_request : ModbusWriteRequest, write_response : ModbusWriteResponse):
    if (write_request.TransactionID == write_response.TransactionID and
        write_request.ProtocolID == write_response.ProtocolID and
        write_request.Length == write_response.Length and
        write_request.UnitID == write_response.UnitID and
        write_request.FunctionCode == write_response.FunctionCode and
        write_request.RegisterAddress == write_response.RegisterAddress):
        return True
    else:
        return False


"""
Provera da li je high alarm aktiviran 
Ako je waterThermometer >=350 aktiviran
To je signal da treba da se control rods spuste u vodu --> posedi kontrol rods na 1,
Kako bi se voda ohladila 
"""


def isHighAlarmActive(waterThermometerAddress, signal_info):
    return int(signal_info[waterThermometerAddress].CurrentValue) >= int(signal_info[waterThermometerAddress].max_alarm)

"""
Proverava da li je low alarm aktiviran 
Ako je waterThermometer <=250 to je znak da se control rods vade iz vode --> podesi control rods na 0 
Kako bi se povecao broj hemijskih reakcija ==> voda se zagreva 
"""


def isLowAlarmActive(waterThermometerAddress, signal_info):
    return int(signal_info[waterThermometerAddress].CurrentValue) <= int(signal_info[waterThermometerAddress].min_alarm)


"""
Function code je uvek 5 posto se manipulise sa control rods -> Digital output 
Formira se WriteRequest nakon cega se salje poruka za promenu stanja control rods-a 
Nakon sto dodje odgovor prepakuje se i proverava se da li ima neka ilegalna f-ja 
Ako nema porede se poslata i primljena poruka i konstatuje se da je vrednost promenjena 
"""


def eOperation(message, fc):
    functionCode = int.from_bytes(message[7:8], byteorder="big", signed=False)
    if fc+128 == functionCode:
        ilegalOperation = int.from_bytes(message[8:9], byteorder="big", signed=False)
        match ilegalOperation:
            case 1:
                print("ILEGAL FUNCTION")
                return True
            case 2:
                print("ILEGAL DATA ACCESS")
                return True
            case 3:
                print("ILEGAL DATA VALUE")
                return True
    else:
        return False


def automation_logic(signal_info, base_info, control_rods_address, command, function_code = 5):
        write_request = ModbusWriteRequest(base_info["station_address"], function_code, signal_info[control_rods_address].start_address,
                                           command)
        response = None
        with Connection.ConnectionHandler.connection_lock:
            if Connection.ConnectionHandler.isConnected:
                if not Connection.ConnectionHandler.isRunning:
                    return
                try:
                    Connection.ConnectionHandler.client.send(write_request.as_bytes())
                    response = Connection.ConnectionHandler.client.recv(1024)
                    if not response:
                        return
                except Exception as e:
                    Connection.ConnectionHandler.isConnected = False
                    Connection.ConnectionHandler.lostConnection.notify_all()
                    print("SCADA DISCONNECTED")
                    print(e)
                    if not Connection.ConnectionHandler.isRunning:
                        return
                    Connection.ConnectionHandler.connected.wait()
                    if not response or not Connection.ConnectionHandler.isRunning:
                        return
        if not response: return
        op = eOperation(response, function_code)
        if op == False:
            modbus_write_response = ModbusWriteResponse.from_bytes(response)
            if compare(write_request, modbus_write_response):
                signal_info[control_rods_address].current_value=command


"""
Vrsi se provera alarma i desava se logika automatizacije 
"""


def automation(signal_info, base_info):
    water_thermometer_address = 2000  # pravi ovo da cita iz signal info
    control_rods_address = 1000
    if isHighAlarmActive(water_thermometer_address, signal_info):
        automation_logic(signal_info, base_info, control_rods_address, 65280)  # #0xFF00 za 1
    elif isLowAlarmActive(water_thermometer_address, signal_info):
        automation_logic(signal_info, base_info, control_rods_address, 0)