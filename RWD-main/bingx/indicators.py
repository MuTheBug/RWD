
import numpy as np
from imports import *
import get_klines


def just_crossed_down(df):
    macd = ta.macd(close=df['close'])
    condition_1 =  macd['MACDh_12_26_9'].iloc[-1] < 0 and macd['MACDh_12_26_9'].iloc[-2]> 0
    condition_2 =  macd['MACDh_12_26_9'].iloc[-2] < 0 and macd['MACDh_12_26_9'].iloc[-3]> 0
    return condition_1 or condition_2

def just_crossed_up(df):
    macd = ta.macd(close=df['close'])
    condition_1 =  macd['MACDh_12_26_9'].iloc[-1] > 0 and macd['MACDh_12_26_9'].iloc[-2]< 0
    condition_2 =  macd['MACDh_12_26_9'].iloc[-2] > 0 and macd['MACDh_12_26_9'].iloc[-3]< 0
    return condition_1 or condition_2

def is_up_trend(df):
    macd = ta.macd(close=df['close'])
    condition_1 =  macd['MACDh_12_26_9'].iloc[-1] > 0 
    condition_2 =  macd['MACDh_12_26_9'].iloc[-1] > macd['MACDh_12_26_9'].iloc[-2] 
    return condition_1 and condition_2

def is_down_trend(df):
    macd = ta.macd(close=df['close'])
    condition_1 =  macd['MACDh_12_26_9'].iloc[-1] < 0 
    condition_2 =  macd['MACDh_12_26_9'].iloc[-1] < macd['MACDh_12_26_9'].iloc[-2] 
    return condition_1 and condition_2