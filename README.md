# Stock-Calendar

I build this because of this video: [Synergy Traders #10.2: "Best Options Strategy We’ve EVER Used!" with Matt Choi](https://www.youtube.com/watch?v=lVIdj3P9Dfc).


#### Disclaimer: I am not clamming that I know the formula used in Matt Choi program, nor is this meant to give finacial advice. This is more only out of interest of data mining and data analisist.



I went to this website to obtain the list of stocks names in the US [gurufocus](https://www.gurufocus.com/stock_list.php).
![image](https://user-images.githubusercontent.com/21014768/129580026-f789fa8b-fcf2-4d5f-9b7a-5a4421b478b8.png)

When it was time to download the data I put the range for about 10 years back of data.
If I ran into problems with obtaining data the job of the bot was to skip that stock.

After all of that I was left with a smaller list of stocks to work with.
Totaling around 7,083 stocks as seen in the [data/raw folder](https://github.com/mymggithub/Stock-Calendar-Bot/tree/main/data/raw).

10,309 stocks that the script identified as companies under 10 years located in the [data/under_min](https://github.com/mymggithub/Stock-Calendar-Bot/tree/main/data/under_min) folder.

# How to use this bot.

This script does all of [Matt Choi steps](https://github.com/mymggithub/Stock-Calendar-Bot/tree/main/saved/manual%20cal#the-steps-matt-choi-recommends-to-get-started-video).

## Requirements
- Python 3
- pandas_datareader, numpy and pandas libraries 
 



