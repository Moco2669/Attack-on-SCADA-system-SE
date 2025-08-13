class Signal:
    def __init__(self, reg_type, num_reg, start_address, min_value, max_value, start_value, signal_type, low_alarm, high_alarm, register_name):
        self._Reg_type = reg_type
        self._Num_reg = num_reg
        self._StartAddress = start_address
        self._MinValue = min_value
        self._MaxValue = max_value
        self._StartValue = start_value
        self._SignalType = signal_type
        self._MinAlarm = low_alarm
        self._MaxAlarm = high_alarm
        self._Name = register_name
        self._AlarmNow = "NO ALARM"
        self.CurrentValue = start_value

    @property
    def alarm(self):
        return self._AlarmNow

    @alarm.setter
    def alarm(self, alarm):
        self._AlarmNow = alarm

    @property
    def name(self):
        return self._Name

    @name.setter
    def name(self, value):
        self._Name = value

    @property
    def reg_type(self):
        return self._Reg_type

    @reg_type.setter
    def reg_type(self, value):
        self._Reg_type = value

    @property
    def num_reg(self):
        return self._Num_reg

    @num_reg.setter
    def num_reg(self, value):
        self._Num_reg = value

    @property
    def start_address(self):
        return self._StartAddress

    @start_address.setter
    def start_address(self, value):
        self._StartAddress = value

    @property
    def min_value(self):
        return self._MinValue

    @min_value.setter
    def min_value(self, value):
        self._MinValue = value

    @property
    def max_value(self):
        return self._MaxValue

    @max_value.setter
    def max_value(self, value):
        self._MaxValue = value

    @property
    def start_value(self):
        return self._StartValue

    @start_value.setter
    def start_value(self, value):
        self._StartValue = value

    @property
    def signal_type(self):
        return self._SignalType

    @property
    def signal_type_string(self):
        if self._SignalType == "DO":
            return "Digital Output"
        elif self._SignalType == "DI":
            return "Digital Input"
        elif self._SignalType == "AO":
            return "Analog Output"
        elif self._SignalType == "AI":
            return "Analog Input"
        else:
            return "Unknown Signal Type"

    @signal_type.setter
    def signal_type(self, value):
        self._SignalType = value

    @property
    def min_alarm(self):
        return self._MinAlarm

    @min_alarm.setter
    def min_alarm(self, value):
        self._MinAlarm = value

    @property
    def max_alarm(self):
        return self._MaxAlarm

    @max_alarm.setter
    def max_alarm(self, value):
        self._MaxAlarm = value

    @property
    def current_value(self):
        return self.CurrentValue

    @current_value.setter
    def current_value(self, value) -> None:
        if value < self._MinValue:
            self.CurrentValue = self._MinValue
        elif value > self._MaxValue:
            self.CurrentValue = self._MaxValue
        else:
            self.CurrentValue = value
        if self._MinAlarm != "NO ALARM" and self._MaxAlarm != "NO ALARM":
            if self.CurrentValue <= self._MinAlarm:
                self.alarm = "LOW ALARM"
            elif self.CurrentValue >= self._MaxAlarm:
                self.alarm = "HIGH ALARM"
            else:
                self.alarm = "NO ALARM"

    def __str__(self):
        return f"Signal Info: Reg_type: {self._Reg_type},Num_reg: {self._Num_reg},StartAddress: {self._StartAddress},MinValue: {self._MinValue},MaxValue: {self._MaxValue},StartV: {self._StartValue},SignalType: {self._SignalType},MinAlarm: {self._MinAlarm},MaxAlarm: {self._MaxAlarm},Name:{self._Name}, CurrentValue:{self.CurrentValue}"
