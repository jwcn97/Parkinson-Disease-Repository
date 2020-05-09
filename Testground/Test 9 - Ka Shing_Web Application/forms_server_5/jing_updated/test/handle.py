import pandas as pd
import numpy as np
from scipy import signal

def cal_mean(c):
    # calculate mean of 3 different tries
    return np.around(np.add.reduceat(c, np.arange(0, len(c), 3))/3,3).round(1)

def get_jitters(df):
    df['discard'] = 0

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

def find_peaks(title, df, d):
    time_p_main = []
    p_plot_main = []
    peaks_main = []
    
    for ax in ['x','y','z','resultant']:
        p, p_prop = signal.find_peaks(df[ax], height=0, distance=d)
        time_p = [df.loc[i,'elapsed (s)'] for i in p]
        p_plot = p_prop['peak_heights']
        peaks = pd.DataFrame({ 'time': time_p, 'peaks': p_plot })

        time_p_main.append(time_p)
        p_plot_main.append(p_plot)
        peaks_main.append(peaks)
    
    return time_p_main, p_plot_main, peaks_main

def find_troughs(title, df, d):
    time_t_main = []
    t_plot_main = []
    troughs_main = []
    
    for ax in ['x','y','z','resultant']:
        t, t_prop = signal.find_peaks(-df[ax], height=0, distance=d)
        time_t = [df.loc[i,'elapsed (s)'] for i in t]
        t_plot = -t_prop['peak_heights']
        troughs = pd.DataFrame({ 'time': time_t, 'peaks': t_plot })

        time_t_main.append(time_t)
        t_plot_main.append(t_plot)
        troughs_main.append(troughs)
    
    return time_t_main, t_plot_main, troughs_main