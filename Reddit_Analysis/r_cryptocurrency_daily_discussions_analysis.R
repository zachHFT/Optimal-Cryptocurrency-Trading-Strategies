library(ggplot2)
library(gganimate)
library(tidyr)
library(dplyr)
library(ggrepel)
library(lubridate)

btc.usd <- read.csv("BTCUSDT-1d-binance.csv")
btc.usd$timestamp <- as.Date(btc.usd$timestamp) #change timestamp to date format
btc.usd <- btc.usd %>% mutate('log_return_close' = c(0, diff(log(close), lag=1))) #add log_close_price


daily_discussions <- read.csv("r_cryptocurrency_daily_discussions.csv")
daily_discussions <- daily_discussions %>% select(-X) %>% #remove extraneous index column
  filter(grepl("Welcome to the Daily Discussion", body) & (author == "AutoModerator")) %>% #isolate official Daily Disucssion threads
  mutate(created = as.Date(created, "%Y-%m-%d")) %>%
  complete(created=seq.Date(min(created), max(created), by="day")) #fill missing days with NA's

str(daily_discussions) 

daily_discussions <- daily_discussions %>% filter(created > "2019-8-3") #data starts here (in earnest); avoids many NA's 
created <- with(daily_discussions, created)

btc.usd <- btc.usd %>% filter(timestamp %in% created) #subset prices accordingly 

df <- data.frame(day=created, score=daily_discussions$score, num_comments=daily_discussions$num_comments,
                 log_return=btc.usd$log_return_close)

p <- ggplot(data=df, aes(x=day, y=log_return)) + geom_line() + #generate plot to be animated
  transition_reveal(day) +
  view_follow() +
  ease_aes("exponential-out") +
  geom_label_repel(aes(label = score),
                   nudge_x = 1,
                   na.rm = TRUE) +
  theme_minimal() 

animate(p)
        #fps  =  [pick how smooth you want],
        #duration = 274, # = 365 days/yr x 3 years x 0.25 sec/day = 274 seconds
        #nframes
        






 





