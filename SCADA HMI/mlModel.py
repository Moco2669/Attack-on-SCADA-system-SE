import time
from threading import Thread
from threading import Event
import xgboost as xgb
import numpy as np
from DataBase import DataBase
from MachineLearning.CommandInjection import CommandInjection
from MachineLearning.FindingState import FindingState
from MachineLearning.NormalState import NormalState
from MachineLearning.ReplayAttack import ReplayAttack


class MachineLearningModel:
    def __init__(self, database: DataBase):
        self.database = database
        self._running = True
        self.connection_event = Event()
        self.controlRodsList = list()
        self.waterThermometerList = list()
        self.register_values_history = list()
        self.counter = 0
        self.same_consecutive_state = 0
        self.system_states_history = list()
        self.xgboostModel = xgb.XGBClassifier()
        self.xgboostModel.load_model('xgb.json')
        self._detection_loop = Thread(target=self.run)
        self._detection_loop.start()
        self.setup_handlers()

    def setup_handlers(self):
        @self.database.event("stop")
        def handle_stop():
            self.stop()

        @self.database.event("scada_connected")
        def handle_scada_connected():
            self.wake_up()

    def run(self):
        while self._running:
            if not self.database.scada_connected:
                self.connection_event.wait()
            self.take_values_for_predict(self.database.registers)
            if len(self.register_values_history) == 6:
                detected_state = self.xgboostModel.predict(np.array(self.register_values_history).reshape(1, 6))
                self.system_states_history.append(detected_state)
                self.same_consecutive_state += 1
                self.register_values_history.clear()
            if self.same_consecutive_state == 2:
                if np.all(self.system_states_history[0] == self.system_states_history[1]):
                    if self.system_states_history[0][0][0] == 1:
                        self.database.update_system_state(ReplayAttack())
                    elif self.system_states_history[0][0][1] == 1:
                        self.database.update_system_state(CommandInjection())
                    elif self.system_states_history[0][0][2] == 1:
                        self.database.update_system_state(NormalState())
                    else:
                        self.database.update_system_state(FindingState())
                self.system_states_history.clear()
                self.same_consecutive_state = 0
            time.sleep(1)

    """
    Uzima poslednje 3 vrednosti za prediktovanje 
    """
    def take_values_for_predict(self, registers: dict):
        if self.counter != 3:
            for register in registers.values():
                match register.signal_type:
                    case "DO":
                        self.controlRodsList.append(register.current_value)
                    case "AI":
                        self.waterThermometerList.append(register.current_value)
            self.counter += 1
        else:
            self.counter = 0
            self.register_values_history.extend(self.waterThermometerList)
            self.register_values_history.extend(self.controlRodsList)
            self.waterThermometerList.clear()
            self.controlRodsList.clear()

    def wake_up(self):
        self.connection_event.set()
        self.connection_event.clear()

    def stop(self):
        self._running = False
        self.wake_up()
        self._detection_loop.join()
        print("Security thread stopped.")