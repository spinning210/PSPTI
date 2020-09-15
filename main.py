from dwh import technical_index, source
import model
import pandas as pd
import numpy as np
from tqdm import tqdm

#此程式處理原始資料，決定要使用的股票代碼，將各家公司分別取出並計算技術指標趨勢
aa = [2330,2317,2412,6505,1301,1303,2454,2882,2881,3008]
for i in tqdm(aa):    
    stock_code = str(i)
    tmp = source.Source(stock_code = stock_code)

    original_ti = technical_index.Technical_index(stock_code + '_original.csv')
    original_ti.company_stock.to_csv(stock_code + '_ti.csv')

    #make a final ti data
    a = technical_index.Ti_convert(stock_code + '_ti.csv')
    a.results.to_csv('data/ti/' + stock_code + '.csv')