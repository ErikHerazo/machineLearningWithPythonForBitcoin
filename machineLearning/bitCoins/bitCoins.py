import json
import os
# external libraries
import pandas as pd
import datetime
import numpy as np
from cryptocmd import CmcScraper

class BitCoin():
    
    palette_btc = {
        'orange': '#f7931a',
        'white' : '#ffffff',
        'gray'  : '#4d4d4d',
        'blue'  : '#0d579b',
        'green' : '#329239'
    }

    btc_halving = {
        'halving': [0, 1 , 2, 3, 4],
        'date': ['2009-01-03', '2012-11-28', '2016-07-09', '2020-05-11', np.nan],
        'reward': [50, 25, 12.5, 6.25, 3.125],
        'halving_block_number': [0, 210000, 420000 ,630000, 840000],
    }

    @classmethod
    def extractAndProcessData(cls, parameterDictionary):
        BTC = parameterDictionary.get("BTC")
        START = parameterDictionary.get("START")
        END = parameterDictionary.get("END")
        scraper = CmcScraper(BTC, START, END)
        data = scraper.get_dataframe()
        data.sort_values(by='Date', ascending=True, inplace=True)
        pd.set_option('display.max_columns', None)
        return data

    @classmethod
    def cleaningAndSavingOfData(cls, data):
        data['date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d %H:%M:%S')
        data = data.loc[:, ['date', 'Open', 'Close', 'High', 'Low']]
        data = data.rename({'Open': 'open', 'Close': 'close', 'High': 'high', 'Low': 'low'}, axis=1)
        data = data.set_index('date')
        data = data.asfreq('D')
        data = data.sort_index()
        data.to_csv('machineLearning/bitCoins/data/data.csv', index=True)
        return data

    @classmethod
    def calculateTheNextHalving(cls, parameterDictionary):
        remaining_blocks = parameterDictionary.get("remaining_blocks")
        blocks_per_day = parameterDictionary.get("blocks_per_day")
        days = remaining_blocks / blocks_per_day
        start_date = parameterDictionary.get("start_date")
        next_halving = pd.to_datetime(start_date, format='%Y-%m-%d') + datetime.timedelta(days=days)
        next_halving = next_halving.replace(microsecond=0, second=0, minute=0, hour=0)
        next_halving = next_halving.strftime('%Y-%m-%d')
        cls.btc_halving['date'][-1] = next_halving
        response = {
            "next_halving_prediction": f'The next halving will occur on approximately: {next_halving}',
        }
        return response

    @classmethod
    def rewardsAndCountdownToNextHalving(cls, data):
        data['reward'] = np.nan
        data['countdown_halving'] = np.nan

        for i in range(len(cls.btc_halving['halving'])-1):            
            # Start and end date of each halving
            if cls.btc_halving['date'][i] < data.index.min().strftime('%Y-%m-%d'):
                start_date = data.index.min().strftime('%Y-%m-%d')
            else:
                start_date = cls.btc_halving['date'][i]
            end_date = cls.btc_halving['date'][i+1]
            mask = (data.index >= start_date) & (data.index < end_date)
            # Fill column 'reward' with mining rewards
            data.loc[mask, 'reward'] = cls.btc_halving['reward'][i]
            # Fill column 'countdown_halving' with remaining days
            time_to_next_halving = pd.to_datetime(end_date) - pd.to_datetime(start_date)
            data.loc[mask, 'countdown_halving'] = np.arange(time_to_next_halving.days)[::-1][:mask.sum()]
        # Check that the data have been created correctly
        # ==============================================================================
        print('Second halving:', cls.btc_halving['date'][2])
        print(data.loc['2016-07-08':'2016-07-09'])
        print('')
        print('Third halving:', cls.btc_halving['date'][3])
        print(data.loc['2020-05-10':'2020-05-11'])
        print('')
        print('Next halving:', cls.btc_halving['date'][4])
        print(data.tail(2))
        # return data

                
data_load_parameters = {
    "BTC":'BTC',
    "START":"03-01-2009",
    "END":"30-05-2023",
}

data_frame = BitCoin.extractAndProcessData(data_load_parameters)
# print(data_frame)

cleaning_data = BitCoin.cleaningAndSavingOfData(data_frame)
# print(cleaning_data)

parameters_netx_halving = {
    "remaining_blocks": 121400,
    "blocks_per_day": 144,
    "start_date": '2022-01-14',
}

next_halving = BitCoin.calculateTheNextHalving(parameters_netx_halving)
# print(next_halving)

reward = BitCoin.rewardsAndCountdownToNextHalving(cleaning_data)
print(reward)