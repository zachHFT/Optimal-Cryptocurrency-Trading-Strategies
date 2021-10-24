library(tidyverse)
library(lubridate)
library(ggplot2)
library(data.table)
library(evd)
library(plotly)

btc.usd <- read.csv("BTCUSDT-1d-binance.csv")
btc.usd$timestamp <- as.Date(btc.usd$timestamp) #change timestamp to date format
btc.usd <- btc.usd %>% 
  mutate("log_return_close" = c(NA, diff(log(close),lag=1))) #add log_return column
#note: to do this, could also use 'shift' from data.table

btc.usd <- na.omit(btc.usd) #omit rows with NA elements due to log transform

btc.usd <- btc.usd %>% mutate(year = format(timestamp, format = "%Y"),
                              dayofyear = yday(timestamp)) #isolate years from timestamp; index the timestamp with a number from 1 to 365

#data from years with data from Jan-Dec
btc.usd_return_18_20 <- btc.usd %>% filter(year %in% c("2018","2019","2020")) %>%
  select(dayofyear, year, log_return_close) %>% group_by(year) %>% spread(year,log_return_close) #tidy data up 

colnames(btc.usd_return_18_20) <- c("dayofyear", "logreturn18", "logreturn19", "logreturn20")

int.plot_return_18_20 <- plot_ly(data=btc.usd_return_18_20, x=~dayofyear, y=~logreturn18, name="2018",
                                 type="scatter", mode="lines")
int.plot_return_18_20 %>% add_trace(y = ~logreturn19, name = '2019', mode = 'lines') %>%
  add_trace(y = ~logreturn20, name = '2020', mode = 'lines') %>% layout(hovermode = "x unified")