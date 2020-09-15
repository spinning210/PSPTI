import csv
from tqdm import tqdm


def ti_to_csv(file, path, name):
    """
    
    Args:
        file: 
        path : 存放路徑
        name : 已存在或是需新增的檔案
    """
    print(name + '.csv is exporting...')

    with open(path + name +'.csv', 'w', newline='') as csvFile:
        fieldNames = ['code','date','open','high','low','close','volume','to','nt','mv','p/e','p/b',
                        'RSV','K','D','J','MACD','MOM','WILLR','MFI','RSI','DX','TRIX','CCI','ROC',
                        'BOLL-U','BOLL-M','BOLL-D']

        writer = csv.DictWriter(csvFile, fieldNames)
        writer.writeheader()

        for i in tqdm(range(0, len(file))):
            writer.writerow({'code' : file.iloc[i]['code'],
                            'date' : file.iloc[i]['date'],
                            'open' : file.iloc[i]['open'],
                            'high' : file.iloc[i]['high'],
                            'low' : file.iloc[i]['low'],
                            'close' : file.iloc[i]['close'],
                            'volume' : file.iloc[i]['volume'],
                            'to' : file.iloc[i]['to'],
                            'nt' : file.iloc[i]['nt'],
                            'mv' : file.iloc[i]['mv'],
                            'p/e' : file.iloc[i]['p/e'],
                            'p/b' : file.iloc[i]['p/b'],
                            'RSV' : file.iloc[i]['RSV'],
                            'K' : file.iloc[i]['K'],
                            'D' : file.iloc[i]['D'],
                            'J' : file.iloc[i]['J'],
                            'MACD' : file.iloc[i]['MACD'],
                            'MOM' : file.iloc[i]['MOM'],
                            'WILLR' : file.iloc[i]['WILLR'],
                            'MFI' : file.iloc[i]['MFI'],
                            'RSI' : file.iloc[i]['RSI'],
                            'DX' : file.iloc[i]['DX'],
                            'TRIX' : file.iloc[i]['TRIX'],
                            'CCI' : file.iloc[i]['CCI'],
                            'ROC' : file.iloc[i]['ROC'],
                            'BOLL-U' : file.iloc[i]['BOLL-U'],
                            'BOLL-M' : file.iloc[i]['BOLL-M'],
                            'BOLL-D' : file.iloc[i]['BOLL-D']})
                            #'' : file.iloc[i][''],