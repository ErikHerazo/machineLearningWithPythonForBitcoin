import json
import os
# external libraries
import yfinance as yf
import pandas as pd
import datetime

class BitCoin():

    @classmethod
    def yahooFinanceDataExtractor(cls, parameterDictionary):
        bitcoin_symbol = parameterDictionary.get("symbol")
        bitcoin_data = yf.Ticker(bitcoin_symbol)
        dataFrame = bitcoin_data.history(start=parameterDictionary.get("start"),
        end=parameterDictionary.get("end"))
        return dataFrame

    @classmethod
    def saveData(cls, parameterDictionary):
        data_frame = parameterDictionary.get('dataFrame')
        print("columnas:--", data_frame.columns)
        path = parameterDictionary.get('path')
        file_name = parameterDictionary.get('fileName')
        csv_data = data_frame.to_csv(f"{path}/{file_name}", index=False)
        response = {
            "message": "data saved successfully",
        }
        return json.dumps(response)


dataLoadParameters = {
    "symbol":'BTC-USD',
    "start":"2019-01-01",
    "end":"2023-06-15",
}

# 'machineLearning/bitCoins/data/dataFrame.csv'
bitcoin_dataframe = BitCoin.yahooFinanceDataExtractor(dataLoadParameters)
print(bitcoin_dataframe)

parameterDictionary = {
    "dataFrame": bitcoin_dataframe,
    "fileName": "csvData.csv",
    "path": "machineLearning/bitCoins/data"
}

data_csv = BitCoin.saveData(parameterDictionary)
print(data_csv)