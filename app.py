from asyncore import read
import streamlit as st
from utils import read_wav
# import numpy as np
# import pandas as pd
import plotly.graph_objects as go

from scipy.fft import fft, ifft
import librosa
import matplotlib.pyplot as plt
import numpy as np
import wave
import streamlit_vertical_slider  as svs

from utils import read_wav




cols = st.columns(2)
with cols[0]:
    # svs.vertical_slider(key="key1", 
    #                 default_value=0, 
    #                 step=1, 
    #                 min_value=0, 
    #                 max_value=100,
    #                 slider_color= 'green', #optional
    #                 track_color='lightgray', #optional
    #                 thumb_color = 'red' #optional
    #                 )
    st.slider( "Sampling Rate",
                min_value=0,
                max_value=100,
                step=1,
                value=2,
                key="sampling_rate00")
with cols[1]:
    st.slider( "Sampling Rate11",
                min_value=int(0),
                max_value=int(100),
                step=1,
                value=2,
                key="sampling_rate0")
    # svs.vertical_slider(key="key2", 
    #                     default_value=0, 
    #                     step=1, 
    #                     min_value=0, 
    #                     max_value=100,
    #                     slider_color= 'green', #optional
    #                     track_color='lightgray', #optional
    #                     thumb_color = 'red' #optional
    #                     )

    
file = st.file_uploader(label="Upload Sound File", key="uploaded_file",type=["wav"])
if not file:
    st.stop()


spf = wave.open(file, "r")
# spf = read_wav(file)

# Extract Raw Audio from Wav File
signal = spf.readframes(-1)
signal = np.fromstring(signal, "int")
fs = spf.getframerate()


Time = np.linspace(0, len(signal) / fs, num=len(signal))
fig = go.Figure()
fig.add_trace(go.Scatter(x=Time,
                                y=signal,
                                mode='lines',
                                name='Signal'))
# plt.figure(1)
# plt.title("Signal Wave...")
# plt.plot(Time, signal)
# plt.show()
st.plotly_chart(fig)



# fig2 = go.Figure()
# fig2.add_trace(go.Scatter(x=Time,
#                                 y=signal,
#                                 mode='lines',
#                                 name='Signal'))
# st.plotly_chart(fig2)
