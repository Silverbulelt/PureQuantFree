import numpy as np
import talib
from purequant import time

class INDICATORS:

    def __init__(self, platform, instrument_id, time_frame):
        self.__platform = platform
        self.__instrument_id = instrument_id
        self.__time_frame = time_frame
        self.__last_time_stamp = 0

    def CurrentBar(self):
        """获取k线数据的长度"""
        records = self.__platform.get_kline(self.__time_frame)
        kline_length = len(records)
        return kline_length

    def HIGHEST(self, length):
        """周期最高价"""
        records = self.__platform.get_kline(self.__time_frame)
        records.reverse()
        kline_length = len(records)
        high_array = np.zeros(kline_length)
        t = 0
        for item in records:
            high_array[t] = item[2]
            t += 1
        result = (talib.MAX(high_array, length))
        return result

    def MA(self, length):
        """
        移动平均线(简单移动平均), 返回值为一个包含各个bar上周期均价的列表
        """
        records = self.__platform.get_kline(self.__time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t+=1
        result = (talib.SMA(close_array, length))
        return result

    def EMA(self, length):
        """指数移动平均线"""
        records = self.__platform.get_kline(self.__time_frame)
        records.reverse()
        kline_length = len(records)
        close_array = np.zeros(kline_length)
        t = 0
        for item in records:
            close_array[t] = item[4]
            t += 1
        result = (talib.EMA(close_array, length))
        return result


    def LOWEST(self, length):
        """周期最低价"""
        records = self.__platform.get_kline(self.__time_frame)
        records.reverse()
        kline_length = len(records)
        low_array = np.zeros(kline_length)
        t = 0
        for item in records:
            low_array[t] = item[3]
            t += 1
        result = (talib.MIN(low_array, length))
        return result

    def VOLUME(self):
        """成交量"""
        records = self.__platform.get_kline(self.__time_frame)
        length = len(records)
        records.reverse()
        t = 0
        volume_array = np.zeros(length)
        for item in records:
            volume_array[t] = item[5]
            t += 1
        return volume_array




