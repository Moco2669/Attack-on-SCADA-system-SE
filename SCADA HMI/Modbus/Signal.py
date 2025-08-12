class Signal:
    def __init__(self, reg_type, num_reg, start_address, min_value, max_value, start_value, signal_type, low_alarm, high_alarm, register_name):
        self._Reg_type = reg_type
        self._Num_reg = num_reg
        self._StartAddress = start_address
        self._MinValue = min_value
        self._MaxValue = max_value
        self._StartV = start_value
        self._SignalType = signal_type
        self._MinAlarm = low_alarm
        self._MaxAlarm = high_alarm
        self._Name = register_name
        self._AlarmNow = "NO ALARM"
        self.CurrentValue = start_value

    def alarm(self):
        return self._AlarmNow

    def Modify_Alrm(self,alarm):
        self._AlarmNow = alarm

    def Name(self):
        return self.Name

    def Name(self,name):
        self.Name = name

    def Reg_type(self):
        return self._Reg_type

    def Reg_type(self, value):
        self._Reg_type = value

    def getNum_reg(self):
        return self._Num_reg

    def setNum_reg(self, value):
        self._Num_reg = value

    Num_reg = property(getNum_reg,setNum_reg)

    def getStartAddress(self):
        return self._StartAddress

    def setStartAddress(self, value):
        self._StartAddress = value

    StartAddress = property(getStartAddress,setStartAddress)

    def MinValue(self):
        return self._MinValue

    def MinValue(self, value):
        self._MinValue = value

    def MaxValue(self):
        return self._MaxValue

    def MaxValue(self, value):
        self._MaxValue = value

    def StartV(self):
        return self._StartV

    def StartV(self, value):
        self._StartV = value

    def getSignalType(self):
        return self._SignalType

    def setSignalType(self, value):
        self._SignalType = value

    SignalType = property(getSignalType,setSignalType)

    def getMinAlarm(self):
        return self._MinAlarm

    def setMinAlarm(self, value):
        self._MinAlarm = value

    MinAlarm = property(getMinAlarm,setMinAlarm)
    def getMaxAlarm(self):
        return self._MaxAlarm
    def setMaxAlarm(self, value):
        self._MaxAlarm = value

    MaxAlarm = property(getMaxAlarm,setMaxAlarm)
    def getcurrentValue(self):
        return self.CurrentValue

    def setcurrentValue(self,value):
        if value < self._MinValue:
            self.CurrentValue = self._MinValue
        elif value > self._MaxValue:
            self.CurrentValue = self._MaxValue
        else:
            self.CurrentValue = value
        if self._MinAlarm != "NO ALARM" and self._MaxAlarm != "NO ALARM":
            if self.CurrentValue <= self._MinAlarm:
                self.Modify_Alrm("LOW ALARM")
            elif self.CurrentValue >= self._MaxAlarm:
                self.Modify_Alrm("HIGH ALARM")
            else:
                self.Modify_Alrm("NO ALARM")

    currentValue = property(getcurrentValue,setcurrentValue)

    def __str__(self):
        return f"Signal Info: Reg_type: {self._Reg_type},Num_reg: {self._Num_reg},StartAddress: {self._StartAddress},MinValue: {self._MinValue},MaxValue: {self._MaxValue},StartV: {self._StartV},SignalType: {self._SignalType},MinAlarm: {self._MinAlarm},MaxAlarm: {self._MaxAlarm},Name:{self._Name}, CurrentValue:{self.CurrentValue}"
