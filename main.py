import pandas_datareader as web
import datetime
import os
import numpy as np
import pandas as pd
from time import sleep

BOT = {"NUM":1, "MAX":5}
START_YR = "2009"
YRS_MIN = 10
FORCE_UPDATE = False
REPASS = False
LAST_POS = True
STOCK_LIST_DIR = "stock_list"
MAX_RANGE = 75
DIR = {
    "DATA": "data",
    "RAW": "data/raw",
    "YRS": "data/yearly",
    "under_min": "data/under_min"
}

if 'BOT' not in globals():
    BOT = {"NUM":1}

if BOT['NUM']>1:
   STOCK_LIST_DIR = "stock_list{}".format(BOT['NUM'])


for k in DIR:
    if not os.path.exists(DIR[k]):
        os.mkdir(DIR[k])
        
d_range = list(range(MAX_RANGE+1))[0::15][1:][::-1]
for r in d_range:
    range_dir = "{}/r_{}".format(DIR['DATA'], r)
    if not os.path.exists(range_dir):
        os.mkdir(range_dir)
    
def set_col(df, c_name, c_type="str", tmp_i="False", v=np.nan):
    if not (c_name in df.columns):
        if c_type == "str":
            df[c_name] = ""
            df[c_name] = df[c_name].astype(str)
        else:
            df[c_name] = np.nan
    if not tmp_i == "False":
        if c_type == "str":
            try:
                df.at[tmp_i, c_name] = ""
            except:
                df[c_name] = ""
                
        df.at[tmp_i, c_name] = v
        

try:
    tickers = pd.read_csv(r'{}.csv'.format(STOCK_LIST_DIR), engine='python')
    tickers = tickers.loc[:, ~tickers.columns.str.contains('^Unnamed')]
except:
    pass
    tickers = pd.DataFrame()
    
t_len = 0
t_len_fixed = 0
START_LIST_NUM = 0
END_LIST_NUM = 0
if "MAX" in BOT and BOT['MAX'] > 0:
    t_len = len(tickers.index)
    t_len_fixed = t_len+[n for n in list(range(BOT['MAX'])) if (t_len+n)%BOT['MAX']==0][0]
    START_LIST_NUM = int((t_len_fixed/BOT['MAX'])*(BOT['NUM']-1))
    if BOT['MAX'] != BOT['NUM']:
        END_LIST_NUM = int((t_len_fixed/BOT['MAX'])*BOT['NUM'])
print("Num:{} Start/Stop {}/{}".format(t_len, START_LIST_NUM+1, END_LIST_NUM+1 if END_LIST_NUM>0 else t_len_fixed))
        
set_col(tickers, 'symbol')
set_col(tickers, 'company')
set_col(tickers, 'price', "int")
set_col(tickers, 'ignore')
set_col(tickers, 'start_yr')
set_col(tickers, 'ignore_error')

if tickers.empty:
    tickers.to_csv(r'{}.csv'.format(STOCK_LIST_DIR))


for i, row in tickers.iterrows():
    if START_LIST_NUM>0 and i<START_LIST_NUM:
        continue
    if END_LIST_NUM>0 and END_LIST_NUM>START_LIST_NUM and i>END_LIST_NUM:
        break
    SYMBOL = row["symbol"]
    
    try:        
        current_stock = pd.read_csv(r'{}/{}_{}.csv'.format(DIR['RAW'], SYMBOL, "history"), index_col=['Date'] , parse_dates=['Date'])
        tickers.at[i, "ignore"] = False
    except:
        current_stock = ""
        
    print(i+1, SYMBOL)
    if (pd.notnull(row['ignore']) and row['ignore'] and not REPASS):
        print("--Ignore: {}".format(row['ignore'] and not REPASS))
        continue
    if FORCE_UPDATE or not str(current_stock):
        print("--get data")
        try:
            current_stock = web.DataReader(SYMBOL, data_source="yahoo", start=START_YR) 
            set_col(tickers, "ignore","str", i, False)
        except Exception as e:
            set_col(tickers, "ignore","str", i, True)
            set_col(tickers, "ignore_error","str", i, e)
            print("---Error: {}".format(e))
            tickers.to_csv(r'{}.csv'.format(STOCK_LIST_DIR))
            continue
    
        

    tickers.at[i, "price"] = current_stock.tail(1)["Close"][0]
    tickers.at[i, "ignore"] = skip = current_stock.tail(1).index[0].year-current_stock.head(1).index[0].year < YRS_MIN
    tickers.at[i, "start_yr"] = current_stock.head(1).index[0].year
    print("--Skip: {}".format(skip))
    if skip:
        current_stock.to_csv(r'{}/{}_{}.csv'.format(DIR["under_min"], current_stock.head(1).index[0].year, SYMBOL))
        tickers.to_csv(r'{}.csv'.format(STOCK_LIST_DIR))
        continue
    else:
#         if REPASS or not os.path.exists(r'{}/{}_{}.csv'.format(DIR['RAW'], SYMBOL, "history")):
        current_stock.to_csv(r'{}/{}_{}.csv'.format(DIR['RAW'], SYMBOL, "history"))

#     if REPASS or not os.path.exists(r'{}/{}_yrs_adj_data.csv'.format(DIR['YRS'], SYMBOL)) or not os.path.exists(r'{}/{}_yrs_close_data.csv'.format(YRS_DIR, SYMBOL)):
    yearly_adj_df = pd.DataFrame()
    yearly_df = pd.DataFrame()
    for j, row2 in current_stock.iterrows():
        yearly_adj_df.at["{:02d}-{:02d}".format(j.month, j.day), j.year] = row2["Adj Close"]
        yearly_df.at["{:02d}-{:02d}".format(j.month, j.day), j.year] = row2["Close"]

    yearly_adj_df.sort_index(inplace=True)
    yearly_df.sort_index(inplace=True)
#     else:
#         yearly_adj_df = pd.read_csv(r'{}/{}_yrs_adj_data.csv'.format(DIR['YRS'], SYMBOL), parse_dates=True, index_col=['Unnamed: 0'], engine='python')
#         yearly_df = pd.read_csv(r'{}/{}_yrs_close_data.csv'.format(DIR['YRS'], SYMBOL), parse_dates=True, index_col=['Unnamed: 0'], engine='python')
        
    r_adj_df_list = {}
    r_c_df_list = {}
    r_pc_df_list = {}
    
    for r in d_range:
        r_adj_df_list[r] = pd.DataFrame()
        r_c_df_list[r] = pd.DataFrame()
        r_pc_df_list[r] = pd.DataFrame()
        for j, row2 in yearly_df.iterrows():
            adj_d_ups = adj_d_downs = c_d_ups = c_d_downs = 0
            for yr in yearly_df.columns:
                d = pd.to_datetime('{}-{}'.format(yr, j), format="%Y-%m-%d", dayfirst=True, errors='coerce')
                r_adj_df_list[r].at[j, yr] = r_c_df_list[r].at[j, yr] = r_pc_df_list[r].at[j, yr] = 0
                if not pd.isnull(d):
                    f = d + datetime.timedelta(days=r)
                    tmp_r_df = current_stock.loc['{}-{:02d}-{:02d}'.format(d.year, d.month, d.day):'{}-{:02d}-{:02d}'.format(f.year, f.month, f.day)]

                    if not tmp_r_df.empty:
                        adj_first_range_num = tmp_r_df.head(3)["Adj Close"].dropna().head(1)[0]
                        c_first_range_num = tmp_r_df.head(3)["Close"].dropna().head(1)[0]              
                        adj_last_range_num = tmp_r_df.tail(3)["Adj Close"].dropna().head(1)[0]
                        c_last_range_num = tmp_r_df.tail(3)["Close"].dropna().head(1)[0]

                        r_adj_df_list[r].at[j, yr] = adj_last_range_num - adj_first_range_num
                        r_c_df_list[r].at[j, yr] = c_last_range_num - c_first_range_num
                        r_pc_df_list[r].at[j, yr] = ((c_last_range_num - c_first_range_num)/c_last_range_num)*100
                        if (adj_last_range_num - adj_first_range_num)>0:
                            adj_d_ups=adj_d_ups+1
                        else:
                            adj_d_downs=adj_d_downs+1

                        if (c_last_range_num - c_first_range_num)>0:
                            c_d_ups=c_d_ups+1
                        else:
                            c_d_downs=c_d_downs+1
                            
            set_col(r_adj_df_list[r], "ups", "int", j, adj_d_ups)
            set_col(r_c_df_list[r], "ups", "int", j, c_d_ups)
            set_col(r_pc_df_list[r], "ups", "int", j, c_d_ups)
            set_col(r_adj_df_list[r], "downs", "int", j, adj_d_downs)
            set_col(r_c_df_list[r], "downs", "int", j, c_d_downs)
            set_col(r_pc_df_list[r], "downs", "int", j, c_d_downs)
            
            set_col(tickers, 'adj_up_start_schedule_r_{}'.format(r))
            set_col(tickers, 'adj_up_end_schedule_r_{}'.format(r))
            set_col(tickers, "adj_ups_r_{}".format(r), "int", i, adj_d_ups)
            set_col(tickers, "adj_downs_r_{}".format(r), "int", i, adj_d_downs)
            set_col(tickers, "close_ups_r_{}".format(r), "int", i, c_d_ups)
            set_col(tickers, "close_downs_r_{}".format(r), "int", i, c_d_downs)
            set_col(tickers, "close_downs_r_{}".format(r), "int", i, c_d_downs)
            
            set_col(r_adj_df_list[r], "end_day_sum","str", j, '{:02d}-{:02d}'.format(f.month, f.day))
            set_col(r_c_df_list[r], "end_day_sum","str", j, '{:02d}-{:02d}'.format(f.month, f.day))
        
        r_adj_df_list[r]['avg'] = r_adj_df_list[r].loc[:, ~r_adj_df_list[r].columns.str.contains('^ups|^downs|^avg|^end_day_sum', na=False)].mean(axis=1)
        r_c_df_list[r]['avg'] = r_c_df_list[r].loc[:, ~r_c_df_list[r].columns.str.contains('^ups|^downs|^avg|^end_day_sum', na=False)].mean(axis=1)
        r_pc_df_list[r]['avg'] = r_pc_df_list[r].loc[:, ~r_pc_df_list[r].columns.str.contains('^ups|^downs|^avg|^end_day_sum', na=False)].mean(axis=1)

        range_dir = "{}/r_{}".format(DIR['DATA'], r)
        r_adj_dir = r'{}/{}_r{}_adj_data.csv'.format(range_dir, SYMBOL, r)
        r_c_dir = r'{}/{}_r{}_c_data.csv'.format(range_dir, SYMBOL, r)
        r_pc_dir = r'{}/{}_r{}_pc_data.csv'.format(range_dir, SYMBOL, r)

        r_adj_df_list[r].sort_index(inplace=True)
        r_adj_df_list[r].to_csv(r_adj_dir)
        r_c_df_list[r].sort_index(inplace=True)
        r_c_df_list[r].to_csv(r_c_dir)
        r_pc_df_list[r].sort_index(inplace=True)
        r_pc_df_list[r].to_csv(r_pc_dir)

        set_col(tickers, "adj_up_start_schedule_r_{}".format(r),"str", i, r_adj_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1).index[0])
        set_col(tickers, "adj_up_end_schedule_r_{}".format(r),"str", i, r_adj_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1)["end_day_sum"][0])
        set_col(tickers, "close_up_start_schedule_r_{}".format(r),"str", i, r_c_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1).index[0])
        set_col(tickers, "close_up_end_schedule_r_{}".format(r),"str", i, r_c_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1)["end_day_sum"][0])
        set_col(tickers, "close_up_percent_avg_r_{}".format(r),"int", i, r_pc_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1)["avg"][0])
    
#     if REPASS or not os.path.exists(r'{}/{}_yrs_adj_data.csv'.format(DIR['YRS'], SYMBOL)):
    yearly_adj_df.to_csv(r'{}/{}_yrs_adj_data.csv'.format(DIR['YRS'], SYMBOL))
#     if REPASS or not os.path.exists(r'{}/{}_yrs_close_data.csv'.format(DIR['YRS'], SYMBOL)):
    yearly_df.to_csv(r'{}/{}_yrs_close_data.csv'.format(DIR['YRS'], SYMBOL))
    tickers.to_csv(r'{}.csv'.format(STOCK_LIST_DIR))
print("Done")