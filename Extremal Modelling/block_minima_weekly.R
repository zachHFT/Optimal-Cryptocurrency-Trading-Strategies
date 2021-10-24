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

btc.usd <- na.omit(btc.usd) #omit rows containing NA values

logreturn_plot <- ggplot(data=btc.usd, aes(x = timestamp, y=log_return_close)) + 
  geom_line(color = "darkorchid4") + 
  labs(title = "Log return of closing price over time",
       subtitle = "Data plotted from August 2017 to August 2018",
       y = "log return",
       x = "Date") +
  scale_x_date(date_labels = "%d-%m-%Y") +
  theme_bw(base_size=10)

logreturn_plot

#interactive plot 
interactive_logreturn_plot <- ggplotly(logreturn_plot, width=750)
interactive_logreturn_plot <- interactive_logreturn_plot %>% 
  style(hovertext=paste('Date : ', btc.usd$timestamp, "<br>Log return : ", btc.usd$log_return_close))

interactive_logreturn_plot

ggplot(data=btc.usd, aes(x = log_return_close)) + geom_histogram(bins=50) + #huge lower tail 
  xlab("Log return") +
  ylab("Frequency") +
  theme_bw(base_size=10)

#evaluate distribution of data without outliers, use standard statistical rule 
outliers <- boxplot.stats(btc.usd$log_return_close)$out
out_ind <- which(btc.usd$log_return_close %in% c(outliers))
btc.usd.clean <- btc.usd[-out_ind, ]
par(mfrow=c(1,2))
hist(btc.usd.clean$log_return_close, main='',
     xlab="Log return", ylab="Frequency")
qqnorm(btc.usd.clean$log_return_close) #v. heavy tailed distribution 
abline(0,1,col='red')

##the data without the outliers still has heavy tails compared to normal,
##use extreme value theory (here applied to 1d data) to study these tails


#block minima approach, consider weekly blocks
btc.usd <- btc.usd[-(1:3),] #remove some data so that num. data points = 7k
mat <- matrix(btc.usd$log_return_close, nrow=7) * 100 #turn into percentages 
neg.minima <- apply(-mat, 2, max) #negative minima

qqplot(qgumbel(c(1:206)/207), neg.minima) 
fit.weekly <- fgev(minima)
fit.weekly

par(mfrow=c(2,2))
plot(fit.weekly)

par(mfrow=c(2,2))
plot(profile(fit.weekly)) #profile likelihoods
confint(profile(fit.weekly)) #confidence interval (strong evidence for Type II evt)

plot(profile(fgev(neg.minima, prob=0.25), "quantile")) #4 week (negative) return level
confint(profile(fgev(neg.minima, prob=0.25), "quantile")) #4 week (negative) return level confidence interval

