import pandas_datareader as web
import datetime
import os
import numpy as np
import pandas as pd

# LAST_POS = True

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

class SC_bot():
    def __init__(self, LIST_FILE="stock_list", START_YR="2009", YRS_MIN=10, FORCE_UPDATE=False, REPASS=False, MAX_RANGE=75, BOT={"NUM":1}, DIR={}):
        self.LIST_FILE = LIST_FILE
        self.BOT = BOT
        self.START_YR = START_YR
        self.YRS_MIN = YRS_MIN
        self.FORCE_UPDATE = FORCE_UPDATE
        self.REPASS = REPASS
        if self.BOT['NUM']>1:
           self.STOCK_LIST_DIR = "stock_list{}".format(self.BOT['NUM'])
        
        if 'DATA' not in DIR:
            DIR['DATA']="data"
        if 'RAW' not in DIR:
            DIR['RAW']="data/raw"
        if 'YRS' not in DIR:
            DIR['YRS']="data/yearly"
        if 'under_min' not in DIR:
            DIR['under_min']="data/under_min"
            
        self.DIR = DIR
        
        for k in DIR:
            if not os.path.exists(DIR[k]):
                os.mkdir(DIR[k])
            
        self.d_range = list(range(MAX_RANGE+1))[0::15][1:][::-1]
        for r in self.d_range:
            range_dir = "{}/r_{}".format(DIR['DATA'], r)
            if not os.path.exists(range_dir):
                os.mkdir(range_dir)
                
                
        self.get_list_csv()
        self.set_range()
        set_col(self.tickers, 'symbol')
        set_col(self.tickers, 'company')
        set_col(self.tickers, 'price', "int")
        set_col(self.tickers, 'ignore')
        set_col(self.tickers, 'start_yr')
        set_col(self.tickers, 'ignore_error')   
        self.make_list_csv()
        self.calc()

    def get_list_csv(self):
        try:
            tickers = pd.read_csv(r'{}.csv'.format(self.LIST_FILE), engine='python')
            self.tickers = tickers.loc[:, ~tickers.columns.str.contains('^Unnamed')]
        except:
            print("Missing {}.csv".format(self.LIST_FILE))
            pass
            self.tickers = pd.DataFrame()
            
            
    def set_range(self):
        t_len = len(self.tickers.index)
        t_len_fixed = 0
        self.START_LIST_NUM = 0
        self.END_LIST_NUM = len(self.tickers.index)-1
        if "MAX" in self.BOT and self.BOT['MAX'] > 0:
            t_len_fixed = t_len+[n for n in list(range(self.BOT['MAX'])) if (t_len+n)%self.BOT['MAX']==0][0]
            self.START_LIST_NUM = int((t_len_fixed/self.BOT['MAX'])*(self.BOT['NUM']-1))
            if self.BOT['MAX'] != self.BOT['NUM']:
                self.END_LIST_NUM = int((t_len_fixed/self.BOT['MAX'])*self.BOT['NUM'])
            print("BOTS Current/Max {}/{}".format(self.BOT['NUM'], self.BOT['MAX']))
        print("Total:{} Start/Stop {}/{}".format(t_len, self.START_LIST_NUM+1, self.END_LIST_NUM+1 if self.END_LIST_NUM>0 else t_len_fixed))

    def make_list_csv(self):
        if not os.path.exists(r'{}.csv'.format(self.LIST_FILE)):
            print("Made {}.csv".format(self.LIST_FILE))
        if self.tickers.empty:
            self.tickers.to_csv(r'{}.csv'.format(self.LIST_FILE))
            
    def get_stock(self, SYMBOL, i=0):
        self.error = False
        try:        
            current_stock = pd.read_csv(r'{}/{}_{}.csv'.format(self.DIR['RAW'], SYMBOL, "history"), index_col=['Date'] , parse_dates=['Date'])
            self.tickers.at[i, "ignore"] = False
        except:
            current_stock = ""
            

        if self.FORCE_UPDATE or not str(current_stock):
            print("--get data")
            try:
                current_stock = web.DataReader(SYMBOL, data_source="yahoo", start=self.START_YR) 
                if not self.tickers.empty:
                    set_col(self.tickers, "ignore","str", i, False)
            except Exception as e:
                if not self.tickers.empty:
                    set_col(self.tickers, "ignore","str", i, True)
                    set_col(self.tickers, "ignore_error","str", i, e)
                    self.tickers.to_csv(r'{}.csv'.format(self.LIST_FILE))
                print("---Error: {}".format(e))
                self.error = True
            
        return current_stock
            
    def calc(self):
        for i, row in self.tickers.iterrows():
            if self.START_LIST_NUM>0 and i<self.START_LIST_NUM:
                continue
            if self.END_LIST_NUM>0 and self.END_LIST_NUM>self.START_LIST_NUM and i>self.END_LIST_NUM:
                break
                
            SYMBOL = row["symbol"]
            print(i+1, SYMBOL)
            if (pd.notnull(row['ignore']) and row['ignore'] and not self.REPASS):
                print("--Ignore: {}".format(row['ignore'] and not self.REPASS))
                continue
            current_stock = self.get_stock(SYMBOL, i)
            if self.error:
                continue


            self.tickers.at[i, "price"] = current_stock.tail(1)["Close"][0]
            self.tickers.at[i, "ignore"] = skip = current_stock.tail(1).index[0].year-current_stock.head(1).index[0].year < self.YRS_MIN
            self.tickers.at[i, "start_yr"] = current_stock.head(1).index[0].year
            print("--Skip: {}".format(skip))
            if skip:
                current_stock.to_csv(r'{}/{}_{}.csv'.format(self.DIR["under_min"], current_stock.head(1).index[0].year, SYMBOL))
                self.tickers.to_csv(r'{}.csv'.format(self.LIST_FILE))
                continue
            else:
        #         if self.REPASS or not os.path.exists(r'{}/{}_{}.csv'.format(self.DIR['RAW'], SYMBOL, "history")):
                current_stock.to_csv(r'{}/{}_{}.csv'.format(self.DIR['RAW'], SYMBOL, "history"))

        #     if self.REPASS or not os.path.exists(r'{}/{}_yrs_adj_data.csv'.format(self.DIR['YRS'], SYMBOL)) or not os.path.exists(r'{}/{}_yrs_close_data.csv'.format(YRS_DIR, SYMBOL)):
            yearly_adj_df = pd.DataFrame()
            yearly_df = pd.DataFrame()
            for j, row2 in current_stock.iterrows():
                yearly_adj_df.at["{:02d}-{:02d}".format(j.month, j.day), j.year] = row2["Adj Close"]
                yearly_df.at["{:02d}-{:02d}".format(j.month, j.day), j.year] = row2["Close"]

            yearly_adj_df.sort_index(inplace=True)
            yearly_df.sort_index(inplace=True)
        #     else:
        #         yearly_adj_df = pd.read_csv(r'{}/{}_yrs_adj_data.csv'.format(self.DIR['YRS'], SYMBOL), parse_dates=True, index_col=['Unnamed: 0'], engine='python')
        #         yearly_df = pd.read_csv(r'{}/{}_yrs_close_data.csv'.format(self.DIR['YRS'], SYMBOL), parse_dates=True, index_col=['Unnamed: 0'], engine='python')

            r_adj_df_list = {}
            r_c_df_list = {}
            r_pc_df_list = {}

            for r in self.d_range:
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

                    set_col(self.tickers, 'adj_up_start_schedule_r_{}'.format(r))
                    set_col(self.tickers, 'adj_up_end_schedule_r_{}'.format(r))
                    set_col(self.tickers, "adj_ups_r_{}".format(r), "int", i, adj_d_ups)
                    set_col(self.tickers, "adj_downs_r_{}".format(r), "int", i, adj_d_downs)
                    set_col(self.tickers, "close_ups_r_{}".format(r), "int", i, c_d_ups)
                    set_col(self.tickers, "close_downs_r_{}".format(r), "int", i, c_d_downs)
                    set_col(self.tickers, "close_downs_r_{}".format(r), "int", i, c_d_downs)

                    set_col(r_adj_df_list[r], "end_day_sum","str", j, '{:02d}-{:02d}'.format(f.month, f.day))
                    set_col(r_c_df_list[r], "end_day_sum","str", j, '{:02d}-{:02d}'.format(f.month, f.day))

                r_adj_df_list[r]['avg'] = r_adj_df_list[r].loc[:, ~r_adj_df_list[r].columns.str.contains('^ups|^downs|^avg|^end_day_sum', na=False)].mean(axis=1)
                r_c_df_list[r]['avg'] = r_c_df_list[r].loc[:, ~r_c_df_list[r].columns.str.contains('^ups|^downs|^avg|^end_day_sum', na=False)].mean(axis=1)
                r_pc_df_list[r]['avg'] = r_pc_df_list[r].loc[:, ~r_pc_df_list[r].columns.str.contains('^ups|^downs|^avg|^end_day_sum', na=False)].mean(axis=1)

                range_dir = "{}/r_{}".format(self.DIR['DATA'], r)
                r_adj_dir = r'{}/{}_r{}_adj_data.csv'.format(range_dir, SYMBOL, r)
                r_c_dir = r'{}/{}_r{}_c_data.csv'.format(range_dir, SYMBOL, r)
                r_pc_dir = r'{}/{}_r{}_pc_data.csv'.format(range_dir, SYMBOL, r)

                r_adj_df_list[r].sort_index(inplace=True)
                r_adj_df_list[r].to_csv(r_adj_dir)
                r_c_df_list[r].sort_index(inplace=True)
                r_c_df_list[r].to_csv(r_c_dir)
                r_pc_df_list[r].sort_index(inplace=True)
                r_pc_df_list[r].to_csv(r_pc_dir)

                set_col(self.tickers, "adj_up_start_schedule_r_{}".format(r),"str", i, r_adj_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1).index[0])
                set_col(self.tickers, "adj_up_end_schedule_r_{}".format(r),"str", i, r_adj_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1)["end_day_sum"][0])
                set_col(self.tickers, "close_up_start_schedule_r_{}".format(r),"str", i, r_c_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1).index[0])
                set_col(self.tickers, "close_up_end_schedule_r_{}".format(r),"str", i, r_c_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1)["end_day_sum"][0])
                set_col(self.tickers, "close_up_percent_avg_r_{}".format(r),"int", i, r_pc_df_list[r].sort_values(['ups', 'avg'], ascending=[False, False]).head(1)["avg"][0])

        #     if self.REPASS or not os.path.exists(r'{}/{}_yrs_adj_data.csv'.format(self.DIR['YRS'], SYMBOL)):
            yearly_adj_df.to_csv(r'{}/{}_yrs_adj_data.csv'.format(self.DIR['YRS'], SYMBOL))
        #     if self.REPASS or not os.path.exists(r'{}/{}_yrs_close_data.csv'.format(self.DIR['YRS'], SYMBOL)):
            yearly_df.to_csv(r'{}/{}_yrs_close_data.csv'.format(self.DIR['YRS'], SYMBOL))
            self.tickers.to_csv(r'{}.csv'.format(self.LIST_FILE))
        print("Done")

        
# if __name__ == "__main__":
#     scb = SC_bot(BOT={"NUM":1})
    
def main():
    pass

if __name__ == "__main__":
    main()
