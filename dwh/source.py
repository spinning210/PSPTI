import pandas as pd
import numpy as np
import csv
from tqdm import tqdm
import re


class Source:
    def __init__(self, stock_name = 'stock_name', stock_code = 'stock_code', n = 1 , gap = 0.03):
        self.__get_stocks() 
        self.__get_company_stock(stock_name, stock_code)
        self.__set_feature(n, gap)
        self.__floating_range(stock_code)

    def __get_stocks(self):
        otc2016 = pd.read_csv('data/OTC2016.csv', thousands = ',') 
        otc2017 = pd.read_csv('data/OTC2017.csv', thousands = ',') 
        otc2018 = pd.read_csv('data/OTC2018.csv', thousands = ',') 
        otc = pd.concat([otc2016, otc2017, otc2018])
        otc['date'] = pd.to_datetime(otc['date']).dt.date

        twse2016 = pd.read_csv('data/TWSE2016.csv', thousands = ',') 
        twse2017 = pd.read_csv('data/TWSE2017.csv', thousands = ',') 
        twse2018 = pd.read_csv('data/TWSE2018.csv', thousands = ',') 
        twse = pd.concat([twse2016, twse2017, twse2018])
        twse['date'] = pd.to_datetime(twse['date']).dt.date
        
        self.stock = pd.concat([twse, otc]).sort_values(by=['date'])

    def __get_company_stock(self, stock_name = 'stock_name', stock_code = 'stock_code'):
        """
        找出指定股價資料，存放在company_stock，兩個參數皆可為空。
        Args:
            stock_name : 個股名稱 ex:台泥
            stock_code : 個股代號 ex:1101 string type
        """
        search_for = [stock_name, stock_code]
        company_stock = self.stock.loc[self.stock['code'].str.contains('|'.join(search_for))]
        self.company_stock = company_stock
        return self.company_stock 

    def __set_feature(self, n = 1 , gap = 0.03):
        """
        找出指定股票第d天與第d+n天相比漲跌特徵，1:漲 -1:跌  0:平，存放在floating
        Args:
            n : 和n天前的股價比對
            gap : 股價浮動百分比
        """
        floating = pd.DataFrame()
        
        for i in range(0,len(self.company_stock)):
            if i == len(self.company_stock) - n:
                break

            amplitude = (float(self.company_stock.iloc[i + n]['close']) - float(self.company_stock.iloc[i]['close'])) / float(self.company_stock.iloc[i]['close'])
            if amplitude >= gap:
                floating = floating.append({'date' : self.company_stock.iloc[i + n]['date'], 'floating': 1 }, ignore_index = True)
            elif amplitude <= -gap:
                floating = floating.append({'date' : self.company_stock.iloc[i + n]['date'], 'floating': -1 }, ignore_index = True)
            else:
                floating = floating.append({'date' : self.company_stock.iloc[i + n]['date'], 'floating': 0 }, ignore_index = True)
        
        self.floating = floating

    def __floating_range(self, stock_code):
        result = pd.merge(self.company_stock, self.floating, on = 'date')
        self.result = result
        self.result.to_csv(stock_code + '_original.csv')

    
    # def set_feature_each_day(self):
    #     """
    #     找出指定股票每日漲跌特徵，不看漲跌百分比，今天比昨天漲就標記為漲，1:漲 -1:跌  0:平，存放在floating
    #     """
    #     floating = pd.DataFrame()
        
    #     for i in range(0,len(self.company_stock)):
    #         if i == len(self.company_stock) - 1:
    #             break

    #         if float(self.company_stock.iloc[i + 1]['收盤價(元)']) > float(self.company_stock.iloc[i]['收盤價(元)']):
    #             floating = floating.append({'date' : self.company_stock.iloc[i + 1]['年月日'], 'floating': 1 }, ignore_index = True)
    #         elif float(self.company_stock.iloc[i + 1]['收盤價(元)']) < float(self.company_stock.iloc[i]['收盤價(元)']):
    #             floating = floating.append({'date' : self.company_stock.iloc[i + 1]['年月日'], 'floating': -1 }, ignore_index = True)
    #         else:
    #             floating = floating.append({'date' : self.company_stock.iloc[i + 1]['年月日'], 'floating': 0 }, ignore_index = True)
        
    #     self.each_floating = floating
    
