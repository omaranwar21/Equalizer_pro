import wave
from scipy.io import wavfile
from scipy.io.wavfile import write
import streamlit as st
import numpy as np
import pandas as pd
import sys
from utils import *
import matplotlib.pyplot as plt
import soundfile as sf
import librosa
import threading
import altair as alt




x, sr = getData()


# st.download_button( label="Download reconstructed data", data=csv, file_name='large_df.csv', mime='text/csv')
# f,ax=init_plot() 

# file =

t=np.array(range(0,len(x)))/(sr)
df = pd.DataFrame({'time' : t, 'signal' : list(x)}, columns = ['time', 'signal'])
# f2,cx=init_plot()
# add_to_plot(cx, t, x)
# show_plot(f2)

frequencies, fourier_signal = fourier(x, sr)
# add_to_plot(ax, frequencies[:len(fourier_signal)], fourier_signal)
# show_plot(f)

t=np.array(range(0,len(fourier_signal )))/(sr)
# f1,bx=init_plot()
inverse = play(fourier_signal)
# add_to_plot(bx, t, inverse)



# df= pd.read_csv("C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\Media\\ECG.csv")
# time = df['time']
# signal = df['values']
# t=np.array(range(0,len(x)))/sr
# plt.figure(figsize=(14,5))

# plt.title("waveform of wave file")
# # plt.plot(t,x , color="blue")
# # plt.plot(time,signal , color="blue")
# plt.xlabel("Time")
# plt.ylabel("amplitude")
# # plt.show()
# add_to_plot(ax,t,x)
# # add_to_plot(ax,time,signal)

# show_plot(f)

# y= np.fft.fft(x)
# # y= np.fft.fft(signal)


# draw= [t,x]
# g,gx=init_plot() 
signal_droped = drop(fourier_signal, frequencies, 5000, 5500 , 0)

# add_to_plot(gx, frequencies[:len(fourier_signal)], signal_droped)
# show_plot(g)

singnal_inversed = play(signal_droped)

# d,dx=init_plot()

# add_to_plot(dx, t, singnal_inversed)
# show_plot(f1)
# show_plot(d)

base = alt.Chart(df).mark_rule().encode(
    x='time',
    y='signal',
    
    # row=alt.Row("a:N", title="Factor A", header=alt.base)
).interactive()

# base1 = alt.Chart(car).mark_rule().encode(
#     x='date:T',
#     y='temp_min:Q',
#     y2='temp_max:Q',
#     color='weather:N',
#     # row=alt.Row("a:N", title="Factor A", header=alt.base)
# ).interactive()



# tpCount     = len(x)
# # tpCount     = len(signal)

# values      = np.arange(int(tpCount))

# timePeriod  = tpCount/sr
# # timePeriod  = time[1] - time[0] 

# frequencies = values/timePeriod
# # fr=np.array(range(0,len(x)))/4
# plt.figure(figsize=(10,5))
# plt.xlabel('freq')
# condition = ((frequencies>344)& (frequencies<1341))

# y[condition]=y[condition]*15   # 0.1 --> slider value

# add_to_plot(ax, frequencies, y)
# show_plot(f)

# inverse=np.fft.ifft(y)


# add_to_plot(ax,t,inverse)

# show_plot(f)



st.altair_chart(base)

write("openS1.wav", sr, singnal_inversed.astype(np.int16))

st.audio("C:\\Users\\Anwar\\Desktop\\SBME 2024\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\Media\\S1.wav")

st.audio("openS1.wav")