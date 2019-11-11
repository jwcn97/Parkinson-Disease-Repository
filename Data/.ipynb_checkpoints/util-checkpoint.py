#!/usr/bin/env python
# coding: utf-8

# # Data Analysis and Visualisation - Utility Functions
# ## 1. Import Libraries

# In[1]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
from scipy.fftpack import fft
from scipy import signal


# ## 2. Helper Functions
# ### 2.1 Data Acquisition Function

# In[2]:


def read_csv_file(path): 
    result = None
    if path.endswith('.csv'): 
        result = pd.read_csv(path)
    return result 


# ### 2.2 Plotting Functions

# In[3]:


def plot_in_3d(df, t = ''):   
    """
    Plots the summation of x-, y-, and z-axes in 3D space

    Parameters
    -----
    df: Pandas dataframe
        dataframe extracted from csv    
    """  
    # Initialize figure and 3d projection
    fig = plt.figure(figsize = [10, 10])
    ax = fig.add_subplot(111, projection = '3d')
    # Label axes
    ax.set(xlabel = df.columns[3], ylabel = df.columns[4], zlabel = df.columns[5], title = t) 
    
    # Get datapoints
    x = df.iloc[:, 3]
    y = df.iloc[:, 4]
    z = df.iloc[:, 5]
    
    # Plot
    ax.plot(x, y, z)
    
#     # Save Plots
#     cnt = 0
#     while os.path.exists('{}{:d}.png'.format(t, cnt)):
#         cnt += 1
#     plt.savefig('{}{:d}.png'.format(t, cnt))
    
def plot_time(df, var = 'x', t = ''):
    """
    Plots the desired parameter against time
    
    Parameters:
    -----
    df: Pandas dataframe
        The pandas dataframe containing the data from the acceleromere
    var: str
        The axis 'x', 'y', 'z' to be plotted; defaults to 'x'
    """
    # Check that var is 'x', 'y', or 'z'
    # Defaults to 'x' if not used
    if var not in axis_listing:
        var = 'x'
    
    # Get data
    time = df.iloc[:, 2]
    data = df.iloc[:, df_column_mapping[var]]
    
    # Initialize figure
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # Label axes
    ax.set(xlabel = df.columns[2], ylabel = df.columns[df_column_mapping[var]], title = t) 
    # Customize the major grid
    ax.grid(b=True, which='both')
    
    # Plot
    ax.plot(time, data)
    
def plot_time_3_axes(df, t = ''):
    """
    Plots all axes into a single plot in the time domain
    
    Parameters:
    -----
    df: Pandas dataframe
        The pandas dataframe containing the data from the acceleromere
    t: title
    """
    # Create mapping lists to enumerate over
    select_cols=[3, 4, 5]
    labels=['x','y','z']
    color_map=['r', 'g', 'b']
    
    # Customise plots
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(xlabel = 'Time (s)', ylabel = 'Acceleration (g)', title = t) 
    ax.grid(b=True, which='both')

    # Plot while enumerating 
    for idx, col in enumerate(select_cols): 
        ax.plot(df.iloc[:, 2], df.iloc[:, col], color_map[idx], label=labels[idx])
        
    ax.legend()
    
#     # Save Plots
#     cnt = 0
#     while os.path.exists('{}{:d}.png'.format(t, cnt)):
#         cnt += 1
#     plt.savefig('{}{:d}.png'.format(t, cnt))
    
def plot_frequency(df, fs, t = ''):
    """
    Plots all axes into a single plot in the frequency domain
    
    Parameters:
    -----
    df: Pandas dataframe
        The pandas dataframe containing the data from the acceleromere
    fs: Sampling frequency (512 Hz by default)
    t: title
    """
    # Create mapping lists
    select_cols=[3, 4, 5]
    labels=['x','y','z']
    color_map=['r', 'g', 'b']
    
    lgth, num_signal=df.shape
    fqy = np.zeros([lgth, num_signal])
    
    # Perform FFT on data and store in matrix
    for idx, col in enumerate(select_cols): 
        fqy[:,idx] = np.abs(fft(df.iloc[:, col]))

    index = np.arange(int(lgth/2))/(int(lgth/2)/(fs/2))
    
    # Customise plots
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(xlabel = 'Frequency (Hz)', ylabel = 'Acceleration (g)', title = t) # xlim = [0, fs/2] 
    ax.grid(b=True, which='both')
    
    # Plot 
    for i in range(3):
        ax.plot(index, fqy[0:int(lgth/2),i], color_map[i], label=labels[i])

    ax.legend()

#     # Save Plots
#     cnt = 0
#     while os.path.exists('{}{:d}.png'.format(t, cnt)):
#         cnt += 1
#     plt.savefig('{}{:d}.png'.format(t, cnt))

def plot_frequency_recursive(df, fs, t = ''):
    """
    Plots all axes into a single plot in the frequency domain
    
    Parameters:
    -----
    df: Pandas dataframe
        The pandas dataframe containing the data from the acceleromere
    fs: Sampling frequency (512 Hz by default)
    t: title
    """
    # Create mapping lists
    labels=['x','y','z']
    color_map=['r', 'g', 'b']
    
    lgth, num_signal=df.shape
    fqy = np.zeros([lgth, num_signal])
    
    # Perform FFT on data and store in matrix
    for i in range(num_signal): 
        fqy[:,i] = np.abs(fft(df[:, i]))

    index = np.arange(int(lgth/2))/(int(lgth/2)/(fs/2))
    
    # Customise plots
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set(xlabel = 'Frequency (Hz)', ylabel = 'Acceleration (g)', title = t) # xlim = [0, fs/2] 
    ax.grid(b=True, which='both')
    
    # Plot 
    for i in range(3):
        ax.plot(index, fqy[0:int(lgth/2),i], color_map[i], label=labels[i])

    ax.legend()


# ### 2.3 Filter Functions

# In[4]:


def median_filter(df, f_size):
    select_cols=[3, 4, 5]
    lgth, num_signal=df.shape
    f_data=np.zeros([lgth, num_signal])
    for idx, col in enumerate(select_cols):
        f_data[:,idx]=signal.medfilt(df.iloc[:,col], f_size)
    return f_data

def freq_filter(df, f_size, cutoff):
    select_cols=[3, 4, 5]
    lgth, num_signal=df.shape
    f_data=np.zeros([lgth, num_signal])
    lpf=signal.firwin(f_size, cutoff, window='hamming')
    for idx, col in enumerate(select_cols): 
        f_data[:,idx]=signal.convolve(df.iloc[:,col], lpf, mode='same')
    return f_data

def freq_filter_recursive(df, f_size, cutoff):
    lgth, num_signal=df.shape
    f_data=np.zeros([lgth, num_signal])
    lpf=signal.firwin(f_size, cutoff, window='hamming')
    for i in range(num_signal):
        f_data[:,i]=signal.convolve(df[:,i], lpf, mode='same')
    return f_data


# ### 2.4 Integration Functions

# In[5]:


# Trapezoidal Integration
def TZ_integration(signal): 
    length = signal.shape
    integral = np.zeros(length)
    
    c = 0
    for idx, _ in enumerate(signal): 
        if idx == 0: 
            integral[idx] = c + signal[idx]
        else: 
            integral[idx] = integral[idx - 1] + integral[idx]
    return integral

# Accumulative Integration (based on TZ integration)
def acc_integration(df): 
    select_cols = [3, 4, 5]
    num_rows, num_cols = df.shape
    int_data = np.zeros(df.shape)
    
    for idx, col in enumerate(select_cols): 
        int_data[:, idx] = TZ_integration(data.iloc[:, col])
    return int_data

# Accumulative Integration (based on TZ integration)
def acc_integration_recursive(df): 
    num_rows, num_cols = df.shape
    int_data = np.zeros(df.shape)
    
    for i in range(num_cols): 
        int_data[:, i] = TZ_integration(df[:, i])
    return int_data


# ### 2.5 Miscellaneous Functions

# In[6]:


# Obtains the directory path of interest
def get_folder_path(foldername):
    """
    :foldername type: string - folder name to search
    :rtype: string - path name of interest
    """
    for dirpath, dirnames, filenames in os.walk(os.getcwd()): 
        for dirname in dirnames: 
            if dirname == foldername: 
                path = os.path.join(dirpath, dirname)
                return path


# ### 2.6 Global Parameters

# In[7]:


# Global Configuration Dictionary for Plot Customisation
# use pylab.rcParams.update(params) to update settings
import matplotlib.pylab as pylab
params = {'lines.linewidth' : 1,
          'legend.fontsize': 'x-large',
          'figure.figsize': (15, 5),
         'axes.labelsize': 'large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'x-large'}

# Frequency presets
fs = 512 # sampling frequency
cutoff = 10 # cut-off frequency


# # Archive

# In[8]:


# df.describe()


# In[9]:


# # Typical Matplotlib Plot Anatomy and Workflow
# # Import Matplotlib as plt
# import matplotlib.pyplot as plt

# # 1. Prepare data
# x = [1, 2, 3, 4]
# y = [10, 20, 25, 30]

# # 2. Create Plots
# fig = plt.figure(figsize = [15, 10])
# ax = fig.add_subplot(111)

# # 3. Plot
# ax.plot(x, y, color = 'lightblue', linewidth = 3)
# ax.scatter([2,4,6], [5,15,25], color = 'darkgreen', marker = '^')

# # 4. Customise Plot
# ax.set_xlim(1, 6.5)
# ax.set(xlabel = 'x-axis', ylabel = 'y-axis', title = 'y versus x graph') 
# ax.grid(b=True, which='both')

# # 5. Save Plot
# # plt.savefig('foo.png')

# # 6. Show Plot
# plt.show()

# """
# # Multiple Plots
# x = arange(5)
# y = np.exp(5)
# plt.figure(1)
# plt.plot(x, y)

# z = np.sin(x)
# plt.figure(2)
# plt.plot(x, z)

# w = np.cos(x)
# plt.figure(1) # Here's the part I need, but numbering starts at 1!
# plt.plot(x, w)
# """