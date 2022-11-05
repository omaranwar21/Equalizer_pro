import numpy as np
from scipy.io import wavfile
import base64
import streamlit as st
import pandas as pd
import wave
import matplotlib.pyplot as plt


#init function to dispaly needed grid
def init_plot():
  f, ax = plt.subplots(1,1,figsize=(10,10))                       
  ax.set_xlabel('Time')              # the x_axis title
  ax.yaxis.set_tick_params(length=5)          # to draw the y-axis line (-) for points
  ax.xaxis.set_tick_params(length=0)          # to draw the y-axis line (-) for points
  ax.grid(c='#D3D3D3', lw=1, ls='--')         #lw represent the line width of the grid
  legend = ax.legend()      
  legend.get_frame().set_alpha(1)
  for spine in ('top', 'right', 'bottom', 'left'):  #control the border lines to be visible or not and the width of them
    ax.spines[spine].set_visible(False)
  return  f,ax

#function to pass the x,y data
def add_to_plot(ax,x,y):
  ax.plot(x,y,alpha=0.7,linewidth=2)  # alpha represent the brightness of the line
#fuction to shaw the plotting
def show_plot(f):
  st.pyplot(f)   


def read_wav(file):
    spf = wave.open(file, "r")
    return spf


def fourier(signal, sampleRate):
    n_samples = len(signal)
    f_hat = np.fft.fft(signal, n_samples)
    l = (len(f_hat))
    f = f_hat[:l]
    tpCount     = len(signal)
    values      = np.arange(int(tpCount))
    timePeriod  = tpCount/sampleRate 
    frequencies = values/timePeriod
    return frequencies, f 


def play(signal):
    inversed_signal = np.fft.ifft(signal)
    return inversed_signal


def drop (signal, frequencies, low, high, ratio):
    condition = ((frequencies>low)& (frequencies<high))
    signal[condition]=signal[condition]*ratio   # 0.1 --> slider value
    return signal

