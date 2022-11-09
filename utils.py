import numpy as np
from scipy.io import wavfile
import base64
import streamlit as st
import pandas as pd
import wave
import matplotlib.pyplot as plt
import librosa
import altair as alt
import  streamlit_vertical_slider  as svs
from itertools import repeat
import plotly.tools as tls

#init function for plotting------------------------------------------------
def init_plot():
  f, ax = plt.subplots(1,1,figsize=(10,10))                      #subplots provides a way to plot multiple plots on a single figure giving a single figure fig with an array of axes ax.
  ax.yaxis.set_tick_params(length=5)                             # to draw the y-axis line (-) for points
  ax.xaxis.set_tick_params(length=0)                             # to draw the y-axis line (-) for points
  ax.grid(c='gray', lw=0.1, ls='--')                             #lw represent the line width of the grid
  legend = ax.legend()                                           #show the label frame
  legend.get_frame().set_alpha(1)
  for spine in ('top', 'right', 'bottom', 'left'):               #control the border lines to be visible or not and the width of them
    ax.spines[spine].set_visible(False)
  return f,ax


#function to pass the arrya of axes ax to the same figure-------------------
def add_to_plot(ax,time,f_amplitude, color, label):
  ax.plot( time , f_amplitude, color, alpha=1, linewidth=2, label=label)  # 'shape' express the color or the shape , alpha represent the brightness of the line


#show the figure with the required plots------------------------------------
def show_plot(f):
    f.set_figwidth(4)
    f.set_figheight(8)
    plotly_fig = tls.mpl_to_plotly(f)    #convert matplotlib figure to plotly_fig for more interactive
    plotly_fig.update_layout(font=dict(size=16), xaxis_title= "Time (second)", yaxis_title= 'Voltage (mV)', showlegend = True)     
    st.plotly_chart(plotly_fig, use_container_width=True, sharing="streamlit")

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

@st.cache (ttl = 1, suppress_st_warning = True, persist = False, show_spinner = False)
def getFile():
  # file = st.file_uploader(label="Upload File", key="uploaded_file",type=["wav"])
  # if 'uploaded_file' not in st.session_state:
  #     file = "C:\Users\Anwar\Desktop\SBME 2024\YEAR 3 (2022-2023)\DSP\Tasks\Task 2 v2\DSP_Task2\Media\S1.wav"
  browseButton_style = f"""    
      <style>
        .css-1plt86z .css-186ux35{{
        display: none !important;
    }}

    .css-1plt86z{{
        cursor: pointer !important;
        user-select: none;
    }}

    .css-u8hs99{{
        flex-direction: column !important;
        text-align: center;
        margin-right: AUTO;
        margin-left: auto;
    }}

    .css-1m59kx1{{
        margin-right: 0rem !important;
    }}
    </style>
    """  
  st.markdown(browseButton_style, unsafe_allow_html=True)  
  x, sr =librosa.load(r"C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\Media\\S1 (mp3cut.net).wav")
  return x, sr


def render_svg(svg):
    """Renders the given svg string."""
    svg=open(svg).read()
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)


def creatSliders (num):
    sliders_cols = []
    sliders_cols = st.columns(list(repeat(1,num)))
    
    for index in range (1, num+1):
        sliders_cols.append("col"+str(index))

    for slider in range(1, num+1):
      with sliders_cols[slider-1]:
          key = "slider_"+str(slider)
          svs.vertical_slider(key = key, 
                    default_value = 0, 
                    step = 1, 
                    min_value = 0, 
                    max_value = 100,
                    slider_color = 'green', 
                    # track_color = 'lightgray',
                    # thumb_color = 'red', 
                    )
