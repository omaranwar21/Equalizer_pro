# Load the required libraries:
from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.signal import find_peaks
from scipy.fftpack import fft
from scipy.io import wavfile



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


#---------------------------------------------------------------------------------------------------------------

f,ax=init_plot()  
# Load the data and calculate the time of each sample
samplerate, signal_time_series = wavfile.read(r'C:\Users\HP Probook\Documents\GitHub\DSP_Task2\Media\S1.wav')
times = np.arange(len(signal_time_series))/float(samplerate)
add_to_plot(ax,times,signal_time_series)
show_plot(f)

f,ax=init_plot()  
single_sample_data = signal_time_series[:samplerate,0]
y_freq = fft(single_sample_data)
N = len(single_sample_data)    # Number of samples
T = 1/single_sample_data # Period
domain = len(y_freq) // 2
x_freq = np.linspace(0, samplerate//2, N//2)

add_to_plot(ax,x_freq,y_freq[:domain])
show_plot(f)

inverse=np.fft.ifft(y_freq)
add_to_plot(ax,times[:inverse[-1]],inverse)
show_plot(f)


# Frequency domain representation
# amplitude = np.abs(scipy.fft.rfft(data))
# frequency = scipy.fft.rfftfreq(len(data), (times[1]-times[0]))
# indices = find_peaks(amplitude)



#---------------------------------------------------------------------------------------------------------------

#upload ECG files 
# uploaded_file = st.file_uploader(label="Upload your Signal",
#         type=['csv', 'xslx'])

#read and prepare the uploded signal data to be plot--------------------------------
# df = pd.read_csv(uploaded_file, nrows=1500)    # read the df from the csv file and store it in variable named df
# time = df['time']                              # time will carry the values of the time 
# signal=df['signal']                            # f_amplitude will carry the values of the amplitude of the signal



