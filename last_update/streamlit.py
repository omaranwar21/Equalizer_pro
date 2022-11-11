from scipy.io import wavfile
from scipy.fft import rfft,irfft, rfftfreq
import numpy as np
from scipy.io.wavfile import write
import streamlit as st
import matplotlib.pyplot as plt

sampling_rate,signal=wavfile.read("DSP_Task2\last_update\WhatsApp Audio 2022-11-11 at 9.49.55 AM.wav")


#t=np.array(range(0,len(signal)))/sampling_rate

#write("ex.wav",sampling_rate, signal.astype(np.int16))
#st.audio("ex.wav")

y= rfft(signal)
x= np.abs(rfftfreq(len(signal),1/sampling_rate))

# x= rfftfreq(len(signal),2/sampling_rate)

# y2=y[0:len(x)]

condition=((x>10000)&(x<1757))

y[condition]=y[condition]*0

y2=irfft(y)

write("ex2.wav",sampling_rate, y2.astype(np.int16))
st.audio('DSP_Task2\last_update\WhatsApp Audio 2022-11-11 at 9.49.55 AM.wav')
st.audio("ex2.wav")