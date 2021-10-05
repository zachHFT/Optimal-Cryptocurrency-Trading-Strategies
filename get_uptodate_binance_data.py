# IMPORTS
import pandas as pd
import math
import os.path
from datetime import datetime
from datetime import date
from dateutil import parser
import pickle
import asyncio
from datetime import timedelta
import dateutil.parser
import json

from binance.client import Client

import api

### API
binance_api_key = api.b_pk    #Enter your own API-key here
binance_api_secret = api.b_sk #Enter your own API-secret here

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
# batch_size = 750 #don't think this is needed anymore
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)
main_directory = '/root/OResearch'


### FUNCTIONS
def minutes_of_new_data(symbol, kline_size, data, source, start, end):
    start_date = start
    end_date = end
    if len(data) > 0:  old = parser.parse(data["timestamp"].iloc[-1])
    elif source == "binance": old = datetime.strptime(start_date, '%d %b %Y')
    if source == "binance": new = datetime.strptime(end_date, '%d %b %Y')
    return old, new


"""Fetch and/or update OHLC historical data from binance"""
def get_all_binance(symbol, kline_size, start, end, save=False):    # check that the starting date is what is expected   
    today = date.today()
    today_date = today.strftime("%d %b %Y")
    start_date = start
    end_date = end
    #print('kline_size:', kline_size)
    os.chdir(main_directory + '/Data/Binance_OHLC') #Going to the OHLCData repository        

    filename = '%s-%s-binance.csv' % (symbol,kline_size)
    if os.path.isfile(filename): data_df = pd.read_csv(filename) # we remove delmiter =','
    else: data_df = pd.DataFrame()
    oldest_point, newest_point = minutes_of_new_data(symbol, kline_size, data_df, source="binance", start=start_date, end=end_date)
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])
    if oldest_point == datetime.strptime(start_date, '%d %b %Y'): print('Downloading all available \'%s\' data for \'%s\'. Wait for a bit..!' % (kline_size, symbol))
    else: print('Downloading \'%d\' minutes of new data available for \'%s\', i.e. \'%d\' instances of \'%s\' data.' % (delta_min, symbol, available_data, kline_size))
    klines = binance_client.get_historical_klines(symbol, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
    data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')
    #actual_start_date = dateutil.parser.parse(data.iloc[0]['timestamp']).strftime('%Y-%m-%d')
    #filename_with_actual_start_date = 'binance-%s-%s-to-%s-%s.csv' % (kline_size, actual_start_date, end_date, symbol)
    if len(data_df) > 0:
        temp_df = pd.DataFrame(data)
        data_df = data_df[:len(data_df) - 1]
        data_df = data_df.append(temp_df)
    else: data_df = data
    data_df.set_index('timestamp', inplace=True)
    if save: data_df.to_csv(filename)
    print('All caught up..!')
    #print(data_df)
    os.chdir(main_directory)
    return filename


""" Getting all tradeable pairs in binance for a designated base_pair """
def get_all_tradeable_pairs(basepair):    
    exchange_info = binance_client.get_exchange_info()
    base_pair = basepair #We choose our basepair
    list_symbols = list() #Initializing empty list

    for elem in exchange_info["symbols"]: 
        if elem['status'] == 'TRADING':
            if base_pair in elem["symbol"][-len(base_pair):]:
                list_symbols.append(elem["symbol"]) 
    return list_symbols


""" Clean the newly updated csv. In particular, we setup timestamp in datetime format, and we select a subset of the columns. We also make sure the data is one group of consecutive date, i.e. there is no other missing dates. """
def clean_csv(filename):    
    df = pd.read_csv(main_directory+'/Data/Binance_OHLC'+'/'+filename)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['time_diff_in_days'] = df.timestamp.diff().dt.days
    df['time_diff_in_min'] = df.timestamp.diff().dt.seconds/60
    #df['time_difference_in_min'] = df['time_difference_in_min'].ne(1.0)
    #df['grp_by_time_difference'] = df.timestamp.diff().dt.days.ne(1).cumsum() #group in period of consecutive days
    #df = df[df['grp_date'] == max(df['grp_date'])] #keep only the last set of data with consecutive days
    df = df[['timestamp', 'open', 'high', 'low', 'close', 'volume', 'time_diff_in_days', 'time_diff_in_min']]
    df.to_csv(main_directory+'/Data/Binance_OHLC'+'/'+filename)
    return df

# """Add a column 'group_by' to spot if there is any discrepency in time differences"""
# def add_time_difference(df, binsize):
#     df=df.copy
#     if bin_size == "1m":
#         df['time_difference'] = df.timestamp.diff().dt.seconds/60
#         df['time_difference_in_min'] = df['grp_date'].ne(1.0)
#     if bin_size == "5m":
#         df['time_difference'] = df.timestamp.diff().dt.seconds/300
#         df['time_difference'] = df['grp_date'].ne(1.0)
#     if bin_size == "1h":
#         df['time_difference'] = df.timestamp.diff().dt.seconds/3600
#         df['time_difference'] = df['grp_date'].ne(1.0)
#     if bin_size == "1d":
#         df['group_by'] = df['time_difference_in_min'].ne(1.0)        
#     return df


""" Add the newly updated infos to data_core for the symbol in question"""
def add_infos_to_data_core(base_pair, df, data_core, symbol, filename, bin_size):
    #To open the last saved version of core_data
    with open(main_directory + '/' +'data_core.json') as json_file:
        data_core = json.load(json_file)

    trading_starting_date = df.iloc[0].timestamp.strftime('%Y-%m-%d %H:%M:%S')
    data_core[base_pair][symbol][bin_size]['trading_starting_date'] = trading_starting_date
    file_end_date = df.iloc[-1].timestamp.strftime("%d %b %Y %H:%M:%S")
    data_core[base_pair][symbol][bin_size]['file_end_date'] = file_end_date
    data_core[base_pair][symbol][bin_size]['csv_filename'] = filename
    
    #To save the new updated version of main
    with open(main_directory + '/' +'data_core.json', 'w') as outfile:
        json.dump(data_core, outfile)    
    return


""" Fetching & Updating historical OHLC Data from Binance. For each symbol, update its csv file with the newest available data points, clean the file as we expect, and update/add infos to its corresponding data_core. """
def update_data_for_basepair(base_pair='USDT', nb_symbols_limit=3, bin_size='1d'):
    os.chdir(main_directory+'/Data/Binance_OHLC')
    list_symbols = get_all_tradeable_pairs(base_pair)
    start_date='10 Aug 2017' #Earliest accessible date is start_date='17 Aug 2017', creation date of Binance
    end_date=datetime.today().strftime('%d %b %Y')
    list_OHLC_symbol_fetched = [] #Intializing empty list of symbol
    list_OHLC_filename_fetched = [] #Intializing empty list of filename
    symbol_and_filename = {"symbol":[],"filename":[]};

    for symbol in list_symbols[:nb_symbols_limit]:
        if 'NEO' not in symbol:
            with open(main_directory + '/' + 'data_core.json') as json_file: #opening json
                data_core = json.load(json_file)
            if base_pair not in data_core:
                data_core[base_pair]= {}
            if symbol not in data_core[base_pair]:
                data_core[base_pair][symbol] = {}        
            if bin_size not in data_core[base_pair][symbol]: 
                data_core[base_pair][symbol][bin_size] = {}
            with open(main_directory + '/' + 'data_core.json', 'w') as outfile: #saving newly update data_core
                json.dump(data_core, outfile)  
            #binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
            filename = get_all_binance(symbol, bin_size, start=start_date, end=end_date, save=True) 
            df = clean_csv(filename)
            add_infos_to_data_core(base_pair, df, data_core, symbol, filename, bin_size) 
    
    print('All %s data successfully up-to-date for %s basepair for the first %i symbols' %(bin_size, base_pair, nb_symbols_limit))
    os.chdir(main_directory)
    return
        

#def main():
#    update_data_for_basepair(base_pair='USDT', nb_symbols_limit=3, bin_size='1d')

#main()
    
if __name__ == '__main__':
    main()