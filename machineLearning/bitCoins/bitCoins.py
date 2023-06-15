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
    def saveData(cls, dataFrame):
        csv_data = dataFrame.to_csv('machineLearning/bitCoins/data/csvData.csv', index=False)
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
print(BitCoin.saveData(bitcoin_dataframe))