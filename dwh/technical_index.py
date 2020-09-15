import pandas as pd
from talib import abstract
import talib
import numpy as np

class Technical_index:
    def __init__(self, file_name):
        
        self.company_stock = pd.read_csv('/Users/adam/code/python/sponti/' + file_name )

        #self.RSV()
        self.KDJ()#
        self.MACD()#
        self.MOM()
        self.WILLR()#
        self.MFI()
        self.RSI()
        self.DX()
        self.TRIX()
        self.CCI()
        self.ROC()
        self.BBANDS()#
        self.ADX()
        self.APO()
        #self.AROON()
        self.CMO()
        self.DI()

    # def RSV(self, t = 9):
    #     self.company_stock['9DAYMAX'] = self.company_stock['high'].rolling(t).max()
    #     self.company_stock['9DAYMIN'] = self.company_stock['low'].rolling(t).min()
    #     self.company_stock['RSV'] = 0
    #     self.company_stock['RSV'] = 100 * (self.company_stock['close'] - self.company_stock['9DAYMIN']) / (self.company_stock['9DAYMAX'] - self.company_stock['9DAYMIN'])

    def KDJ(self):#(933)
        kd = abstract.STOCH(self.company_stock, fastk_period = 9)
        
        self.company_stock['K'] = kd['slowk']
        self.company_stock['D'] = kd['slowd']
        self.company_stock['J'] = 3 * self.company_stock['D'] - 2 * self.company_stock['K']
        # print(self.company_stock)

    def MACD(self):#
        macd = abstract.MACD(self.company_stock)

        self.company_stock['EMA12'] = abstract.EMA(self.company_stock, timeperiod = 12)
        self.company_stock['EMA26'] = abstract.EMA(self.company_stock, timeperiod = 26)
        self.company_stock['DIF'] = self.company_stock['EMA12'] - self.company_stock['EMA26']
        self.company_stock['MACD'] = macd['macd']
        self.company_stock['MACDsignal'] = macd['macdsignal']
        self.company_stock['MACDhist'] = macd['macdhist']

    def MOM(self):#10
        mom = abstract.MOM(self.company_stock, timeperiod = 10)

        self.company_stock['MOM'] = mom

    def WILLR(self):#7
        willr = abstract.WILLR(self.company_stock, timeperiod = 14)

        self.company_stock['WILLR'] = willr

    def MFI(self):#26
        self.company_stock['volume'] = self.company_stock['volume'].astype(float)
        mfi = abstract.MFI(self.company_stock, timeperiod = 26)

        self.company_stock['MFI'] = mfi
        
    def RSI(self):#6
        rsi = abstract.RSI(self.company_stock, timeperiod = 6)

        self.company_stock['RSI'] = rsi
    
    def DX(self):#Directional Movement Index 14  可能要重算取中間數值
        dx = abstract.DX(self.company_stock, timeperiod = 14)

        self.company_stock['DX'] = dx
    
    def TRIX(self):#n = 30  可能要重算取中間數值
        trix = abstract.TRIX(self.company_stock, timeperiod = 30)

        self.company_stock['TRIX'] = trix

    def CCI(self):#14
        cci = abstract.CCI(self.company_stock, timeperiod = 14)

        self.company_stock['CCI'] = cci
        #print(self.company_stock)

    def ROC(self):#12
        roc = abstract.ROC(self.company_stock, timeperiod = 12)

        self.company_stock['ROC'] = roc

    def BBANDS(self):#BOLL timeperiod = 5 , nbdevup = 2, nbdevdn = 2, matype = 0(simple moving average)
        bbands = abstract.BBANDS(self.company_stock, timeperiod = 5)

        self.company_stock['BOLL_U'] = bbands['upperband']
        self.company_stock['BOLL_M'] = bbands['middleband']
        self.company_stock['BOLL_D'] = bbands['lowerband']

    def ADX(self):
        adx = abstract.ADX(self.company_stock, timeperiod=14)

        self.company_stock['ADX'] = adx

    def APO(self):
        apo = abstract.APO(self.company_stock,fastperiod=12, slowperiod=26, matype=0)

        self.company_stock['APO'] = apo

    def AROON(self):
        aroondown, aroonup = abstract.AROON(self.company_stock)

        self.company_stock['AROON_U'] = aroonup
        self.company_stock['AROON_D'] = aroondown

        return aroondown, aroonup

    def CMO(self):
        cmo = abstract.CMO(self.company_stock, timeperiod=14)

        self.company_stock['CMO'] = cmo

    def DI(self):
        minus_di = abstract.MINUS_DI(self.company_stock, timeperiod=14)
        plus_di = abstract.PLUS_DI(self.company_stock, timeperiod=14)

        self.company_stock['MINUS_DI'] = minus_di
        self.company_stock['PLUS_DI'] = plus_di

    def ALL(self):
        self.company_stock = self.company_stock.drop('code', axis = 1)
        self.company_stock = self.company_stock.set_index('date')
        self.company_stock = self.company_stock.astype('float')
        df = self.company_stock

        ta_list = talib.get_functions()

        for x in ta_list:
            try:
                output = eval('abstract.'+x+'(df)')
                output.name = x.lower() if type(output) == pd.core.series.Series else None
                df = pd.merge(df, pd.DataFrame(output), left_on = df.index, right_on = output.index)
                df = df.set_index('key_0')
            except:
                print(x, ' error')

        return df
    


class Ti_convert:
    def __init__(self, file_name):
        '''
        跌、賣、空頭、市場處於超買狀況  記做-1
        漲、買、多頭、市場處於超賣狀況  記做 1
        無特徵       記做 0
        '''
        self.ti = pd.read_csv('/Users/adam/code/python/sponti/' + file_name).dropna().tail(600)
        self.results = pd.DataFrame()
        self.__floating_and_date()
        self.__KDJ()
        self.__MACD()
        self.__BBANDS()
        self.__WILLR()
        #self.results.to_csv('1101.csv')

    def __floating_and_date(self):
        floating = self.ti.floating.tolist()
        self.results['floating'] = floating

        date = self.ti.date.tolist()
        self.results['date'] = date
        self.results.set_index('date' , inplace=True)



    def __KDJ(self):
        #v1.若 K 值 > D 值，表示處於漲勢
        self.results['KDJ_K>D'] = self.__KDJ_binary_mark(self.ti.K > self.ti.D, 'up') 
        #v2.若 K 值 < D 值，表示處於跌勢
        self.results['KDJ_K<D'] = self.__KDJ_binary_mark(self.ti.K <= self.ti.D, 'down') 
        #v3.K 值和 D 值，數值皆介於 0%~100% 之間，50% 為多空平衡位置;80% 以上為「超買區」（Overbought Zone），多頭強勢；20% 以下為「超賣區」（Oversold Zone），空頭強勢。
        self.results['KDJ_KD_feature'] = self.__KDJ_kd_feature()
        #v4*.KD黃金交叉，建議買進 - 當 KD 指標的 K 值由下往上突破 D 值，建議買進做多
        #*5.KD死亡交叉，建議賣出 - 當 KD 指標的 K 值由上往下跌破 D 值時，建議賣出做空
        self.results['KDJ_cross'] = self.__KDJ_cross()
        #v6*.當價格與隨機指標發生牛勢背離（即價格下跌而隨機指標指向上方），而 %K 線與 %D 線在超賣區（低於 20%）發生交叉，便是買入信號；反之則是賣出信號。
        self.results['KDJ_div'] = self.__KDJ_divergence()
        #v7*.J值出現超過100，則表示出現頭部，後續股價易有快速下跌的情況
        self.results['KDJ_J>100'] = self.__KDJ_j_mark(self.ti.J >= 100, 'down')
        #v8*.J值出現低於0的情況，則表示出現底部，後續股價反轉向上的機會相當高
        self.results['KDJ_J<0'] = self.__KDJ_j_mark(self.ti.J <= 0, 'up')
        
        #print(self.results)

    def __KDJ_binary_mark(self, mask, r):
        if r == 'down':
            m = -1
            nm = 1
        else:
            m = 1
            nm = -1

        mask = mask.tolist()
        results = []
        for i in mask:
            if i == True:
                results.append(m)
            else:
                results.append(nm)
        return results

    def __KDJ_kd_feature(self):
        up_mask = ((self.ti.K > 80) & (self.ti.D > 80) & (self.ti.K < 100) & (self.ti.D < 100)).tolist()
        down_mask = ((self.ti.K < 20) & (self.ti.D < 20) & (self.ti.K > 0) & (self.ti.D > 0)).tolist()
        results = np.zeros(len(up_mask))
        for i in range(len(up_mask)):
            if up_mask[i] == True:
                results[i] = 1
            if down_mask[i] == True:
                results[i] = -1
        return results

    def __KDJ_divergence(self):
        results = []
        for i in range(len(self.ti)):
            if i == 0:
                results.append(0)
            else:
                if i + 1 == len(self.ti):
                    results.append(0)
                    break
                else:
                    tmp = float(self.ti.iloc[i + 1]['close']) - float(self.ti.iloc[i]['close'])
                    if tmp > 0: #當價格與隨機指標發生牛勢背離 (價格下跌而隨機指標指向上方)
                        if self.results['KDJ_KD_feature'][i] == -1 and self.results['KDJ_cross'][i] != 0: #而 %K 線與 %D 線在超賣區（低於 20%）發生交叉，便是買入信號
                            results.append(1)
                        else:
                            results.append(0)
                    else:#當價格與隨機指標發生牛勢背離 (價格上漲而隨機指標指向下方)
                        if self.results['KDJ_KD_feature'][i] == 1 and self.results['KDJ_cross'][i] != 0: #而 %K 線與 %D 線在超買區（高於 80%）發生交叉，便是賣出信號
                            results.append(-1)
                        else:
                            results.append(0)
        return results
                   
    def __KDJ_cross(self):
        tmp = -2
        cross = []
        cross_data = self.__KDJ_binary_mark(self.ti.K > self.ti.D, 'up' ) #1to0代表k向下跌破d   賣出(跌）
        for i in range(len(cross_data)):
            if cross_data[i] != tmp:
                if i == 0:
                    cross.append(0)
                    tmp = cross_data[i]
                else:
                    if cross_data[i] < tmp :
                        cross.append(-1)
                    else:
                        cross.append(1)
                    tmp = cross_data[i]
            else:
                cross.append(0)
        return cross
    
    def __KDJ_j_mark(self, mask, r):
        if r == 'down':
            m = -1
        else:
            m = 1

        mask = mask.tolist()
        results = []

        for i in mask:
            if i == True:
                results.append(m)
            else:
                results.append(0)

        return results
    
    def __MACD(self):
        #v1.當MACD與DIF值皆為正數，此時為多頭行情。
        self.results['MACD_MDpos'] = self.__MACD_binary_mark((self.ti.MACD > 0) & (self.ti.DIF > 0), 'up')
        #v2.當MACD與DIF值皆為負數，此時為空頭行情。
        self.results['MACD_MDneg'] = self.__MACD_binary_mark((self.ti.MACD < 0) & (self.ti.DIF < 0), 'down')
        #v3*.DIF向上穿越MACD時為買進訊號。 
        #v4*.DIF向下穿越MACD時為賣出訊號。 
        self.results['MACD_cross'] = self.__MACD_cross()
        #v5、分析DIF-MACD柱形圖，由正變負時往往指示該賣，反之往往為買入信號
        self.results['MACD_hist_pn'] = self.__MACD_hist_pn()

    def __MACD_binary_mark(self, mask, r):
        if r == 'up':
            m = 1
        else :
            m = -1
        mask = mask.tolist()
        results = []
        for i in mask:
            if i == True:
                results.append(m)
            else:
                results.append(0)
        return results
    
    def __MACD_cross(self):
        tmp = -2
        cross = []
        cross_data = self.__MACD_binary_mark(self.ti.DIF < self.ti.MACD, 'up') #dif 低於 macd 記1
        for i in range(len(cross_data)):
            if cross_data[i] != tmp:
                if i == 0:
                    cross.append(0)
                    tmp = cross_data[i]
                else:
                    if cross_data[i] < tmp :
                        cross.append(-1)
                    else:
                        cross.append(1)
                    tmp = cross_data[i]
            else:
                cross.append(0)
        return cross

    def __MACD_hist_pn(self):
        tmp = -2
        hist = self.ti.MACDhist.tolist()
        hist_p_to_n = []
        for i in range(len(hist)):
            if i == 0:
                tmp = hist[i]
                hist_p_to_n.append(0)
            else:
                if hist[i] - tmp > 0 : #分析DIF-MACD柱形圖，由正變負時往往指示該賣
                    hist_p_to_n.append(-1)
                    tmp = hist[i]
                else:
                    hist_p_to_n.append(1)
                    tmp = hist[i]
        return hist_p_to_n

    def __BBANDS(self):#boll
        #v1.價格在中軌MID與上軌UPER之間波動運行時為多頭市場,以回調中軌附近做多的操作思路為主
        self.results['BOLL_mu'] = self.__BBANDS_inside_range(((self.ti.close >= self.ti.BOLL_M) & (self.ti.close <= self.ti.BOLL_U)), 'up')
        #v2.價格在中軌MID與下軌LOWER之間向下波動運行時為空頭市場,此時反彈至中軌附近做空為主
        self.results['BOLL_md'] = self.__BBANDS_inside_range(((self.ti.close >= self.ti.BOLL_D) & (self.ti.close <= self.ti.BOLL_M)), 'down')
        #v3*.價格長時間在中軌與上軌UPER之間運行後,由上向下跌破中軌為賣出信號
        #v4*.價格長時間在中軌與下軌LOWER之間運行後,由下向上突破中軌為買入信號   **是否修改長時間條件？
        self.results['BOLL_cross'] = self.__BBANDS_maintain_and_change(((self.ti.close >= self.ti.BOLL_M) & (self.ti.close <= self.ti.BOLL_U)), 'up', 5)
        #5*.布林中軌經長期盤整後轉平並向上拐頭,且價格在中軌之上。此時,若價格回調,其回調至中軌附近就是做多的時機(買進)
        #6*.布林中軌經長期盤整後轉平並向下拐頭，且價格運行在中軌之下。此時,若價格反彈,其反彈至中軌附近是做空機會(賣出)
        
        #v7*.股價碰到上軌道，出場訊號
        self.results['BOLL_over_h'] = self.__BBANDS_over((self.ti.close >= self.ti.BOLL_U), 'down')
        #v8*.股價碰到下軌道，進場訊號
        self.results['BOLL_over_d'] = self.__BBANDS_over((self.ti.close <= self.ti.BOLL_D), 'up')
        #(self.results)

    def __BBANDS_inside_range(self, mask, r):
        if r == 'up':
            m = 1
        else:
            m = -1
        results = []
        mask = mask.tolist()
        for i in mask:
            if i == True:
                results.append(m)
            else:
                results.append(0)
        return results

    def __BBANDS_maintain_and_change(self, mask, r, n = 1 ): 
        tmp = -2
        cross = []
        cross_data = self.__BBANDS_inside_range(mask, 'up') #價格在中軌MID與上軌UPER之間記1
        for i in range(len(cross_data)):
            if cross_data[i] != tmp:
                if i == 0:
                    cross.append(0)
                    tmp = cross_data[i]
                else:
                    if cross_data[i] < tmp :
                        cross.append(-1)
                    else:
                        cross.append(1)
                    tmp = cross_data[i]
            else:
                cross.append(0)
        return cross

    def __BBANDS_over(self, mask, r):
        if r == 'up':
            m = 1
        else:
            m = -1 

        mask = mask.tolist()
        results = []
        for i in mask:
            if i == True:
                results.append(m)
            else:
                results.append(0)
        return results

    def __WILLR(self):
        #v1*.-80%以下則被視為超賣訊號
        self.results['WILLR_d'] = self.__WILLR_over((self.ti.WILLR <= -80), 'down')
        #v2*.超過-20%的水平會視為超買的訊號
        self.results['WILLR_h'] = self.__WILLR_over((self.ti.WILLR >= -20), 'up')
        #v3*.當W%R由下方的超賣區向上爬而穿過中軸 -50% 時，表示開始轉勢，由弱變強，買入
        self.results['WILLR_turns'] = self.__WILLR_turn_strong()
        #v4*.超買區向下跌落，跌破 -50% 中軸線後，可確認強市轉弱，是賣出的訊號。
        self.results['WILLR_turnw'] = self.__WILLR_turn_weak()

    def __WILLR_over(self, mask, r):
        mask = mask.tolist()
        if r == 'up':
            m = 1
        else:
            m = -1

        results = []
        for i in mask:
            if i == True:
                results.append(m)
            else:
                results.append(0)
        return results
        
    def __WILLR_turn_strong(self):
        tmp_under = [] #< -80 的index
        tmp_raising = []
        results = []
        
        for i in range(len(self.ti)) :
            if self.ti.iloc[i]['WILLR'] <= -80 :
                tmp_under.append(i)
        
        for i in range(len(tmp_under)):
            if i + 1 >= len(tmp_under):#最後一個不管
                break
            for j in range(tmp_under[i + 1] - tmp_under[i]):
                if j + tmp_under[i] >= len(self.ti):
                    break
                if self.ti.iloc[j + tmp_under[i]]['WILLR'] >= -50:
                    tmp_raising.append(j + tmp_under[i])
        
        #補最後一個低於-80的日子後的轉勢
        for i in range(tmp_under[len(tmp_under)-1],len(self.ti)):
            if self.ti.iloc[i]['WILLR'] >= -50:
                    tmp_raising.append(i)

        for i in range(len(self.ti)):
            if i in tmp_raising:
                results.append(1)
            else:
                results.append(0)

        return results

    def __WILLR_turn_weak(self):
        tmp_higher = [] #> -20 的index
        tmp_raising = []
        results = []
        
        for i in range(len(self.ti)) :
            if self.ti.iloc[i]['WILLR'] >= -20 :
                tmp_higher.append(i)
        
        for i in range(len(tmp_higher)):
            if i + 1 >= len(tmp_higher):#最後一個不管
                break
            for j in range(tmp_higher[i + 1] - tmp_higher[i]):
                if j + tmp_higher[i] >= len(self.ti):
                    break
                if self.ti.iloc[j + tmp_higher[i]]['WILLR'] <= -50:
                    tmp_raising.append(j + tmp_higher[i])
        
        for i in range(tmp_higher[len(tmp_higher)-1],len(self.ti)):
            if self.ti.iloc[i]['WILLR'] <= -50:
                    tmp_raising.append(i)

        for i in range(len(self.ti)):
            if i in tmp_raising:
                results.append(-1)
            else:
                results.append(0)
        
        return results










