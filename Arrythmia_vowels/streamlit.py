from scipy.io import wavfile
from scipy.fft import rfft,irfft, rfftfreq
import numpy as np
from scipy.io.wavfile import write
import streamlit as st
import matplotlib.pyplot as plt

sampling_rate,signal=wavfile.read("abc.wav")

t=np.array(range(0,len(signal)))/sampling_rate


#write("ex.wav",sampling_rate, signal.astype(np.int16))
#st.audio("ex.wav")

y= rfft(signal)
x= rfftfreq(len(signal),1/sampling_rate)
print(len(y))
print(len(x))

y2=y[0:len(x)]

#for i in range (int(len(x)/2)):
#    x[i]=x[i]*5


condition=((x>14000)&(x<15000))

y2[condition]=y2[condition]*0

y2=irfft(y2)

write("ex2.wav",sampling_rate, y2.astype(np.int16))
st.audio("ex2.wav")