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
