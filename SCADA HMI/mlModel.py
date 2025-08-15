import time
from threading import Thread

import pandas as pd
import xgboost as xgb
import numpy as np
from Connection import ConnectionHandler
from DataBase import DataBase

pdDf = pd.read_csv('learningDataNew.csv')
pdDf.head()

class MachineLearningModel:
    def __init__(self, database: DataBase, connection: ConnectionHandler):
        self.database = database
        self.connection = connection
        self.detection_running = True
        self.controlRodsList = list()
        self.waterThermometerList = list()
        self.predictionList = list()
        self.counter = 0
        self.systemStateCounter = 0
        self.systemStatePrevious = list()
        self.xgboostModel = xgb.XGBClassifier()
        self.xgboostModel.load_model('xgb.json')
        self._detection_loop = Thread(target=self.run)
        self._detection_loop.start()

    def run(self):
        while self.detection_running:
            self.take_values_for_predict(self.database.registers)
            if len(self.predictionList) == 6:
                pred = self.xgboostModel.predict(np.array(self.predictionList).reshape(1, 6))
                self.systemStatePrevious.append(pred)  # dodacu predikciju da proveravam
                self.systemStateCounter += 1
                self.predictionList.clear()
            if self.systemStateCounter == 2 and np.all(self.systemStatePrevious[0] == self.systemStatePrevious[1]):
                if self.systemStatePrevious[0][0][0] == 1:
                    self.database.system_state = "REPLAY ATTACK"
                elif self.systemStatePrevious[0][0][1] == 1:
                    self.database.system_state = "COMMAND INJECTION"
                elif self.systemStatePrevious[0][0][2] == 1:
                    self.database.system_state = "NORMAL STATE"
                else:
                    self.database.system_state = "FINDING STATE"
                self.systemStatePrevious.clear()
                self.systemStateCounter = 0
            elif self.systemStateCounter == 2 and np.any(self.systemStatePrevious[0] != self.systemStatePrevious[1]):
                self.systemStatePrevious.clear()
                self.systemStateCounter = 0
            time.sleep(1)

    """
    Uzima poslednje 3 vrednosti za prediktovanje 
    """
    def take_values_for_predict(self, signal_info: dict):
        if self.counter != 3:
            for key, value in signal_info.items():
                match signal_info[key].signal_type:
                    case "DO":
                        self.controlRodsList.append(signal_info[key].current_value)
                    case "AI":
                        self.waterThermometerList.append(signal_info[key].current_value)
            self.counter += 1
        else:
            self.counter = 0
            self.predictionList.extend(self.waterThermometerList)
            self.predictionList.extend(self.controlRodsList)
            self.waterThermometerList.clear()
            self.controlRodsList.clear()

    def stop(self):
        self.detection_running = False
        self._detection_loop.join()
        print("Security thread stopped.")