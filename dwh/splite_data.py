import numpy as np
import pandas as pd
from tqdm import tqdm

df = pd.read_csv('1101.csv', index_col='date')

def save_splite_data(df,i):
    df.to_csv('data/x/1101_' + str(i) + '_x.csv')

def save_splite_y(df,i):
    df.to_csv('data/y/1101_' + str(i) + '_y.csv')

for i in tqdm(range(len(df))):
    if len(df) > 30:
        save_splite_data(df.head(30),i)
        save_splite_y(df.iloc[30],i)
        df.drop(df.head(1).index, inplace=True)