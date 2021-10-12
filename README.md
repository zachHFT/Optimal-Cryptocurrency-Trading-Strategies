# Optimal-Cryptocurrency-Trading-Strategies
Statistical Data Analysis of Optimal Trading Strategies (Buy-and-Sell) for Cryptocurrencies

The goal of this project is to proceed to the analysis of an optimal trading (buy-and-sell) strategy for the market of Cryptocurrencies. We expect such a strategy, if sucessful, also applicable to the case of traditionnal stock markets.

(note: Cryptocurrencies data are traditionnaly more easily and freely available than stock markets data, which are often pricey)

The first part of the project will consist in showing you how to access the data of all historical data available on Binance.
We choose Binance because it is one, if not the only exchange, with a properly working API which also have historical data up to 2017 and for the widest range of cryptocurrency pairs, and therefore the most diverse range of applicable trading strategy (arbitrage, sentiment-driven prices, trends, market making, etc).

## Data Extraction

To extract the Data, kindly refer to : https://github.com/zachHFT/Get_OHLC_Data/blob/main/Get_OHLC_from_Binance_API/get_data.py
Do not forget to add the "def main():" as well as "if main == __name__ :" at the end of the file.

## Data Cleaning

We use the clean_csv() function to clean the newly doownloaded data file. In particular, we setup timestamp in datetime format, and we select a subset of the columns. We keep the following columns: 'timestamp', 'open', 'high', 'low', 'close', 'volume', 'time_diff_in_days', 'time_diff_in_min'.

Note that I have never encountered any NA values or other seemingly out-of-place values that would need to be rejected. However we do have to be careful and consider the following. Every once in a while there is a major crash in cryptocurrencies market. This leads to everyone trying to connect to the brokers platforms to try to sell (or buy) cryptocurrencies, resulting in the exchange becoming unavailable due to their server crashing as well. Usually all platforms crashes, not a single one resist the massive amount of people trying to connect. This leads to unavailable trading data for some small period of time. Nonetheless, since we are dealing with Time Series type of data, this needs to be taken into account. Therefore we compute the two columns 'time_diff_in_days' and 'time_diff_in_min' to spot any possible jump in the timestamp.

You can find the code used in the get_uptodate_binance_data.py file
