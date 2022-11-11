from scipy.io import wavfile
from scipy.fft import rfft,irfft, rfftfreq
import numpy as np
from scipy.io.wavfile import write
import streamlit as st
import matplotlib.pyplot as plt

sampling_rate,signal=wavfile.read("abc_no_music-_AudioTrimmer.com_.wav")

t=np.array(range(0,len(signal)))/sampling_rate

#ersmii nos el signal m3 adha mn el t 

#write("ex.wav",sampling_rate, signal.astype(np.int16))
#st.audio("ex.wav")

y= rfft(signal)
x= rfftfreq(len(signal),2/sampling_rate)

y2=y[0:len(x)]

condition=((x>1100)&(x<2000))

y2[condition]=y2[condition]*0

y2=irfft(y2)

write("ex2.wav",sampling_rate, y2.astype(np.int16))
st.audio("ex2.wav")