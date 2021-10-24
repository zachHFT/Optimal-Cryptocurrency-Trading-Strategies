library(tidyverse)
library(lubridate)
library(ggplot2)
library(data.table)
library(evd)

btc.usd <- read.csv("BTCUSDT-1d-binance.csv")
btc.usd$timestamp <- as.Date(btc.usd$timestamp) #change timestamp to date format
btc.usd <- btc.usd %>% 
  mutate("log_return_close" = c(NA, diff(log(close),lag=1))) #add log_return column
#note: to do this, could also use 'shift' from data.table

btc.usd <- na.omit(btc.usd) #omit rows with NA elements due to log transform

btc.usd <- btc.usd %>% mutate(year = format(timestamp, format = "%Y"),
                              dayofyear = yday(timestamp)) #isolate years from timestamp; index the timestamp with a number from 1 to 365

#plot data from years with data from Jan-Dec
btc.usd %>% filter(year %in%  c("2018", "2019", "2020")) %>%
  ggplot(aes(x=dayofyear, y = log_return_close)) + 
  geom_line(color = "darkorchid4") +
  facet_wrap( ~ year, ncol=1) +
  labs(title = "Log return of closing price over time",
       subtitle = "Data plotted by year",
       y = "log return",
       x = "Day") + 
  theme_bw(base_size = 10)


  