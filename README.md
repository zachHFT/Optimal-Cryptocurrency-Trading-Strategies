# Optimal-Cryptocurrency-Trading-Strategies


## Team members
zachHFT

yacinetrad

coolsocket

KC0710

1 member missing

## Introduction

Statistical Data Analysis of Optimal Trading Strategies (Buy-and-Sell) for Cryptocurrencies

- The goal of this project is to proceed to the analysis of an optimal trading (buy-and-sell) strategy for the market of Cryptocurrencies. We expect such a strategy, if sucessful, also applicable to the case of traditionnal stock markets.
(note: Cryptocurrencies data are traditionnaly more easily and freely available than stock markets data, which are often pricey)

- The first part of the project will consist in showing you how to access the data of all historical data available on Binance.
We choose Binance because it is one, if not the only exchange, with a properly working API which also have historical data up to 2017 and for the widest range of cryptocurrency pairs, and therefore the most diverse range of applicable trading strategy (arbitrage, sentiment-driven prices, trends, market making, etc).

## Data Extraction

- To extract the Data, you can do so as per the call of get_uptodate_binance_data.update_data_for_basepair(base_pair='USDT', nb_symbols_limit=5, bin_size='1d') in get_ohlc_historical_data.ipynb

- The data will be saved in a folder named 'Binance_OHLC' located within a 'Data' folder within your project folder. If you do not have such folders, create some. (If you are familiar with chdir python function to change and work with your choice directory you can ignore this remark).

- The code in get_uptodate_binance_data.py contains a global variable 'main_directory' which has the name of my project folder I am working on. I recommend you call your project folders with the same name.

- If you don't want to get your hands dirty (which is understandable) navigating through the code to download the data, simply download a set of the date at this link: https://drive.switch.ch/index.php/s/URDxQbEv8LqSkB2

## Data Cleaning

- We use the clean_csv() function to clean the newly doownloaded data file. In particular, we setup timestamp in datetime format, to allow us to have an easier handling of the data later on.

- We also select a subset of the columns of interest to us. In particular we keep keep the following columns: ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'time_diff_in_days', 'time_diff_in_min'].

- Note that we have never encountered any NA values or other seemingly out-of-place values that would need to be rejected. Indeed, so called 'out-of-place values' or any other outliers kind of value are strong indicators which require further investigations and may be relevant to dedicated algorithmic trading strategies. We absolutely do not want to remove them as we may be tempted to do in some other contexts in data science.

- Discrepencies in the timestamp of our data : Missing time periods. Every once in a while there is a major crash in cryptocurrencies market (i.e. prices dropping significantly). This leads to a massive amount of people trying to connect to the cryptocurrencies exchange platforms to try to sell (or buy) some cryptocurrencies.This often results in the exchange becoming unavailable, their server not being able to handle so many connections attempts at once. This explains the missing data in historical cryptocurrencies prices data (It can be for a couple of minutes up to a couple of hours). We therefore compute 'time_diff_in_days' and 'time_diff_in_min' to spot any such discrpencies in the timestamp.


You can find the code in the get_uptodate_binance_data.py file

## Multiple Datasets Analysis

- Once an analysis is performed on a dedicated dataset (e.g. 1 hour BTC-USDT historical data), the same statistical analysis can be performed over any dataset (e.g. 1 minute ETH - CHF historical data), since the data structure (i.e. the columns, open, high, low, close).

- We downloaded the data for hundreds of cryptocurrency pairs over various timeframe (1 day, 1 hour,  1 minute, etc) so that we can perform meta-analysis and/or repeat the small single-pair dataset analysis over all other sets

## Data Enrichment & Feature Engineering

## Feature Selection

## Predictive models


