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

![image](https://user-images.githubusercontent.com/21014768/130071447-7887499a-37fa-41d0-9548-1782f8cbb073.png)

### 2. Put in the ticker symbol. 

![image](https://user-images.githubusercontent.com/21014768/130071854-60ec0462-9465-4e1a-9708-6f89384283a3.png)

### 3. Click Historical Data. 

![image](https://user-images.githubusercontent.com/21014768/130072203-ce8da3a5-77a6-4cd3-b480-38c1f90586e4.png)

### 4. Put a range and click apply. 

![image](https://user-images.githubusercontent.com/21014768/130072549-0a2c3d33-5a3b-4a74-9b73-d1c12e04284d.png)


### 5. Then you will get a download, then he says the improtant data is the "Data" and "Adj Close". 

![image](https://user-images.githubusercontent.com/21014768/130072740-94805825-804c-4d69-8893-cf27634b15fc.png)

### 6. He pivots the Adj close with excel. 
(What I ended up doing was having the script do it for me) results in [data/yearly](https://github.com/mymggithub/Stock-Calendar-Bot/tree/main/data/yearly)

![image](https://user-images.githubusercontent.com/21014768/130072913-e7f6c91e-9855-4a99-959d-3caf0b6b95dc.png)

### 7. Scan the excel. 

![image](https://user-images.githubusercontent.com/21014768/130073081-3977afbf-48a6-46c3-9ea5-a5ce891471a4.png)


### 8. His Conclusion. 

![image](https://user-images.githubusercontent.com/21014768/130073405-0c6e4ae0-b4f7-402c-ac3a-46076fee4aef.png)

![image](https://user-images.githubusercontent.com/21014768/130073576-037c3299-039e-43a3-9ca9-e086de9cccdd.png)

