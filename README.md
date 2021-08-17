# Stock-Calendar-Bot

I build this because of this video originally [Best Options Strategy We've Ever Used! | Matt Choi, CMT](https://www.youtube.com/watch?v=vHnQMTl5jkQ), but the video now has been marked private. 

Here is others videos that provide about the same idea of the original video:

[Synergy Traders #13.07: Predicting Favorable Outcomes For Options Trades with Matt Choi](https://www.youtube.com/watch?v=RAzuPtb2JUg)

[Synergy Traders #10.2: "Best Options Strategy We’ve EVER Used!" with Matt Choi](https://www.youtube.com/watch?v=lVIdj3P9Dfc)



#### Disclaimer: I am not clamming that I know the formula used in Matt Choi program, nor is this meant to give finacial advice. This is more only out of interest of data mining and data analisist.



I went to this website to obtain the list of stocks names in the US [gurufocus](https://www.gurufocus.com/stock_list.php).
![image](https://user-images.githubusercontent.com/21014768/129580026-f789fa8b-fcf2-4d5f-9b7a-5a4421b478b8.png)

When it was time to download the data I put the range for about 10 years back of data.
If I ran into problems with obtaining data the job of the bot was to skip that stock.

After all of that I was left with a smaller list of stocks to work with.
Totaling around 7,083 stocks as seen in the [data/raw folder](https://github.com/mymggithub/Stock-Calendar-Bot/tree/main/data/raw)


# The Steps Matt Choi recommends to get started.

### 1. Go to yahoo finance. 

![vlcsnap-2021-08-17-11h53m31s830](https://user-images.githubusercontent.com/21014768/129774105-6a2974f3-c432-4bd6-85f8-be1cff3e9fbf.png)

### 2. Put in the ticker symbol. 

![vlcsnap-2021-08-17-11h53m36s911](https://user-images.githubusercontent.com/21014768/129774182-68e35393-59e5-4575-9888-706aac205c59.png)

### 3. Click Historical Data. 

![vlcsnap-2021-08-17-11h54m09s535](https://user-images.githubusercontent.com/21014768/129774426-fd5f2c0e-2bcd-46c9-8231-9b295b39b69d.png)

### 4. Put a range and click apply. 

![vlcsnap-2021-08-17-11h54m17s720](https://user-images.githubusercontent.com/21014768/129774647-4f064823-da5b-40d1-b0cb-1a64521483ab.png)

### 5. Then you will get a download, then he says the improtant data is the "Data" and "Adj Close". 

![vlcsnap-2021-08-17-11h54m31s864](https://user-images.githubusercontent.com/21014768/129774764-6e0df486-a86b-4538-92ec-80e8571dd5df.png)


### 6. He pivots the Adj close with excel. 
(What I ended up doing was having the script do it for me) results in [data/yearly](https://github.com/mymggithub/Stock-Calendar-Bot/tree/main/data/yearly)

![vlcsnap-2021-08-17-11h55m11s576](https://user-images.githubusercontent.com/21014768/129775900-649b5297-28cf-46c8-8ef8-dedefb2fdb9f.png)

### 7. Scan the excel. 

![vlcsnap-2021-08-17-11h55m27s990](https://user-images.githubusercontent.com/21014768/129776244-6aedd226-b603-4775-8d44-73cbe6374adb.png

### 8. His Conclusion. 

![vlcsnap-2021-08-17-11h56m06s035](https://user-images.githubusercontent.com/21014768/129776582-211b4123-67dc-43c4-9bb6-b2dce679522c.png)

![vlcsnap-2021-08-17-11h57m05s972](https://user-images.githubusercontent.com/21014768/129776591-9df435e0-18a5-405b-8b72-e64bcacac575.png)
