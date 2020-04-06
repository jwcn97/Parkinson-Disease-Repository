import pandas as pd
import numpy as np
from scipy import signal

def cal_mean(c):
    # calculate mean of 3 different tries
    return np.around(np.add.reduceat(c, np.arange(0, len(c), 3))/3,3).round(1)

def get_jitters(df):
    df['discard'] = 0
    
    for i, row in df.iterrows():
        pos_mean = np.mean(df[df['peaks'] > 0].peaks)
        neg_mean = np.mean(df[df['peaks'] < 0].peaks)

        for i, row in df.iterrows():
            if df.loc[i, 'peaks'] > 0:
                if df.loc[i, 'peaks'] > pos_mean:
                    df.at[i, 'discard'] = 1
            elif df.loc[i, 'peaks'] < 0:
                if df.loc[i, 'peaks'] < neg_mean:
                    df.at[i, 'discard'] = 1
    
    return df[df['discard'] == 0]

def peak_cols(title):
    if 'ftap' in title:
        col = 'x'
        # if 'Accelerometer' in title: col = 'z'
        # elif 'Gyroscope' in title:   col = 'y'
    elif 'hmove' in title:
        col = 'x'
        # if 'Accelerometer' in title: col = 'z'
        # elif 'Gyroscope' in title:   col = 'y'
    elif 'tota' in title:
        col = 'z'
        # col = 'y'

    return col

def find_peaks(title, df, d):
    # return threshold values depending on dataset
    col = peak_cols(title)
    
    p, p_prop = signal.find_peaks(df[col], height=0, distance=d)
    time_p = [df.loc[i,'elapsed (s)'] for i in p]
    p_plot = p_prop['peak_heights']

    peaks = pd.DataFrame({ 'time': time_p, 'peaks': p_plot })
    
    return time_p, p_plot, peaks, col

def find_troughs(title, df, d):
    # return threshold values depending on dataset
    col = peak_cols(title)
    
    t, t_prop = signal.find_peaks(-df[col], height=0, distance=d)
    time_t = [df.loc[i,'elapsed (s)'] for i in t]
    t_plot = -t_prop['peak_heights']

    troughs = pd.DataFrame({ 'time': time_t, 'peaks': t_plot })
    
    return time_t, t_plot, troughs, col