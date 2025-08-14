import time
import pandas as pd
import sklearn.model_selection
import xgboost as xgb
import numpy as np
import sklearn as skl
from xgboost import XGBClassifier
import Connection
from Acquisition import StateHolder
from DataBase import DataBase

pdDf = pd.read_csv('learningDataNew.csv')
pdDf.head()

class MachineLearningModel:
    def __init__(self, database: DataBase):
        self.database = database
        self.controlRodsList = list()
        self.waterThermometerList = list()
        self.predictionList = list()
        self.counter = 0
        self.systemStateCounter = 0
        self.systemStatePrevious = list()
        self.xgboostModel = xgb.XGBClassifier()
        self.xgboostModel.load_model('xgb.json')

    def run(self):
        while Connection.ConnectionHandler.isRunning:
            self.take_values_for_predict(self.database.registers)
            if len(self.predictionList) == 6:
                pred = self.xgboostModel.predict(np.array(self.predictionList).reshape(1, 6))
                self.systemStatePrevious.append(pred)  # dodacu predikciju da proveravam
                self.systemStateCounter += 1
                self.predictionList.clear()
            if self.systemStateCounter == 2 and np.all(self.systemStatePrevious[0] == self.systemStatePrevious[1]):
                if self.systemStatePrevious[0][0][0] == 1:
                    StateHolder.state = "REPLAY ATTACK"
                elif self.systemStatePrevious[0][0][1] == 1:
                    StateHolder.state = "COMMAND INJECTION"
                elif self.systemStatePrevious[0][0][2] == 1:
                    StateHolder.state = "NORMAL STATE"
                else:
                    StateHolder.state = "FINDING STATE"
                self.systemStatePrevious.clear()
                self.systemStateCounter = 0
            elif self.systemStateCounter == 2 and np.any(self.systemStatePrevious[0] != self.systemStatePrevious[1]):
                self.systemStatePrevious.clear()
                self.systemStateCounter = 0
            if not Connection.ConnectionHandler.isConnected:
                if not Connection.ConnectionHandler.isRunning:
                    break
                with Connection.ConnectionHandler.connection_lock:
                    Connection.ConnectionHandler.connected.wait()
            time.sleep(1)
        print("Security thread stopped.")

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