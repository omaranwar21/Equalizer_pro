# Load the required libraries:
from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np
import streamlit as st
import scipy.fft
from scipy.signal import find_peaks


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
samplerate, data = wavfile.read(r'D:\DSP_Task2\Media\S2.wav')
times = np.arange(len(data))/float(samplerate)


# Frequency domain representation
# amplitude = np.abs(scipy.fft.rfft(data))
# frequency = scipy.fft.rfftfreq(len(data), (times[1]-times[0]))
# indices = find_peaks(amplitude)


add_to_plot(ax,times,data)

show_plot(f)