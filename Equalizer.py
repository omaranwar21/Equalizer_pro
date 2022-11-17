import streamlit as st
from   utils import *    
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import librosa
import librosa.display
import math
import time
import IPython.display as ipd
import streamlit.components.v1 as components
from streamlit.components.v1 import html
import matplotlib.pyplot as plt
import pygame
from pydub import AudioSegment
from just_playback import Playback
from replit import audio
import os
from scipy.fft import rfft,irfft, rfftfreq
import scipy.signal
import streamlit_nested_layout


# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Equalizer",
    page_icon="🔉",
    layout="wide"
)


with open("style.css") as design:
    st.markdown(f"<style>{design.read()}</style>", unsafe_allow_html=True)


parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(parent_dir, "build")
_vertical_slider = components.declare_component("vertical_slider", path=build_dir)

def vertical_slider(value, step, min=min, max=max, key=None):
    slider_value = _vertical_slider(value = value,step = step, min = min, max = max, key = key, default = value)
    return slider_value

# ----------------------------------------------------------------------------

def init_plot():
  f, ax = plt.subplots(1,1,figsize=(10,10))                       
  ax.set_xlabel('Time')                       # the x_axis title
  ax.yaxis.set_tick_params(length=5)          # to draw the y-axis line (-) for points
  ax.xaxis.set_tick_params(length=0)          # to draw the y-axis line (-) for points
  ax.grid(c='#D3D3D3', lw=1, ls='--')         #lw represent the line width of the grid
  legend = ax.legend()      
  legend.get_frame().set_alpha(1)
  for spine in ('top', 'right', 'bottom', 'left'):  #control the border lines to be visible or not and the width of them
    ax.spines[spine].set_visible(False)  
  return  f,ax


#function to pass the x,y data------------------------------------------------
def add_to_plot(ax,x,sr):
  ax.specgram(x,Fs = sr)  # alpha represent the brightness of the line



#fuction to shaw the plotting--------------------------------------------------
def show_plot(f):
        st.pyplot(f)   


# -----------------------------------------------------------------------------
def sampled_signal(signal, time):
    pack = 100
    sampled_time= time[::pack]
    sampled_signal= signal[::pack]
    return sampled_signal, sampled_time


# -----------------------------------------------------------------------------
def plot_altair(firstDataFrame, secondDataframe, cutoff):
    plot_width = 1000
    end = firstDataFrame["time"].iloc[-1] + 0.05

    zoom = alt.selection_interval(
    bind='scales',
    on="[mousedown[!event.shiftKey], mouseup] > mousemove",
    translate="[mousedown[!event.shiftKey], mouseup] > mousemove!",
    )

    selection = alt.selection_interval(
        on="[mousedown[event.shiftKey], mouseup] > mousemove",
        translate="[mousedown[event.shiftKey], mouseup] > mousemove!",
    )

    selector = alt.selection_single(
        name="SelectorName",
        fields=["cutoff"],
        init={"cutoff": cutoff},
    )

    ############################  First Graph  ############################
    firstGraph = alt.Chart(firstDataFrame).mark_rule().encode(
            x=alt.X('time', axis=alt.Axis(title=None, labelColor='white', titleColor='white', domainColor='#132346'), scale=alt.Scale(domain=(0, end))),
            y=alt.Y('signal', axis=None),
            color = alt.condition(alt.datum["time"] < selector["cutoff"],
                    alt.value("#ffffff"), alt.value("#595959"))
        ).properties(
            width=plot_width,
            height=200
        ).add_selection(
            selector,
            zoom,
            selection
        )

    ############################  second Graph  ############################
    secondGraph = alt.Chart(secondDataframe).mark_rule().encode(
            x=alt.X('time', axis=alt.Axis(title='Time', labelColor='white', titleColor='white', domainColor='#132346'), scale=alt.Scale(domain=(0, end))),
            y=alt.Y('signal', axis=None),
            color = alt.condition(alt.datum["time"] < selector["cutoff"],
                    alt.value("#ffffff"), alt.value("#595959"), legend=alt.Legend(title=" "))
        ).properties(
            width=plot_width,
            height=200
        ).add_selection(
            selector,
            zoom,
            selection
        )

    ############################  Figure Displaying  ############################
    firstChart= firstGraph.encode()
    secondChart= secondGraph.encode()

    figure = alt.vconcat(firstChart, secondChart).configure_axisX(
        gridColor = '#00e0ff',
        domainColor = 'white',
        titleColor = '#ffffff'
    ).configure(
        background = '#132346',
        padding = {"left": 0, "top": 0, "right": 0, "bottom": 0}
    ).configure_view(
        strokeWidth = 5,
        fill ='#074a7e',
        stroke='#132346'
    )

    return figure

# ---------------------------------------------------------------------------------------------------
def start_Plotting (time, line_plot, step, Audio_dataFrame, edited_Audio_dataFrame):
    for st.session_state.i in np.arange(st.session_state.i, math.ceil(time[-1]), step):
        lines = plot_altair(Audio_dataFrame, edited_Audio_dataFrame, st.session_state.i)
        line_plot = line_plot.altair_chart(lines)

def fourier_transform(signal,sr):
    y_sig= scipy.fft.rfft(signal)
    mag=np.abs(y_sig)
    phase=np.angle(y_sig)
    freq= rfftfreq(len(signal),1/sr)
    return mag,phase,freq 

def invers (new_mag,phase):
    signal=np.multiply(new_mag,np.exp(1j*phase))
    inv_fourier_signal = np.real(scipy.fft.irfft(signal))
    return inv_fourier_signal

# convert the signals after sampling to data frame
def plot_init(t_sampled, first_signal_sampled, second_signal_sampled):
    Audio_dataFrame = pd.DataFrame({'time' : t_sampled, 'signal' : list(first_signal_sampled)}, columns = ['time', 'signal'])
    edited_Audio_dataFrame = pd.DataFrame({'time' : t_sampled, 'signal' : list(second_signal_sampled)}, columns = ['time', 'signal'])
    lines = plot_altair(Audio_dataFrame, edited_Audio_dataFrame, st.session_state.i)
    line_plot = st.altair_chart(lines)
    return line_plot, Audio_dataFrame, edited_Audio_dataFrame


def drop(first_index, last_index, values_list, freq, new_mag):
    max_freq = max(freq)
    # st.write(max_freq)
    Ranges = {
        '0': [[0 , max_freq/10]],
        '1': [[max_freq/10 , 2*(max_freq/10)]],
        '2': [[2*(max_freq/10) , 3*(max_freq/10)]],
        '3': [[3*(max_freq/10) , 4*(max_freq/10)]],
        '4': [[4*(max_freq/10) , 5*(max_freq/10)]],
        '5': [[5*(max_freq/10) , 6*(max_freq/10)]],
        '6': [[6*(max_freq/10) , 7*(max_freq/10)]],
        '7': [[7*(max_freq/10) , 8*(max_freq/10)]],
        '8': [[8*(max_freq/10) , 9*(max_freq/10)]],
        '9': [[9*(max_freq/10) , max_freq]],

        '10': [[9*(max_freq/10) , max_freq]],
        '11': [[9*(max_freq/10) , max_freq]],
        '12': [[9*(max_freq/10) , max_freq]],
        '13': [[9*(max_freq/10) , max_freq]],

        '14': [[9*(max_freq/10) , max_freq]],
        '15': [[9*(max_freq/10) , max_freq]],
        '16': [[9*(max_freq/10) , max_freq]]
    }

    # dictionary = dict()
    # for key, val in Ranges.items():
    #     if int(key) >= first_index and int (last_index) <= last_index:
    #         dictionary[key] = val

    # st.write(Ranges[0])

    for (key, value) in enumerate(Ranges.items()):
        # st.write(first_index)
        # st.write(last_index)
        # st.write(slider)
        
        slider_ranges = value[1]
        # st.write (slider_ranges)
        # st.write(values_list) 
        if (key < len(values_list)):
            # st.write(key)
            for drop in slider_ranges:
                # st.write(drop)
                index=np.where((freq>drop[0])&(freq<drop[1]))
                triangle_window=10**(values_list[key]*scipy.signal.windows.triang(len(index)))
                # hanning_window=10**(values_list[slider]*np.hanning(len(index)))
                # st.write(hanning_window)
                # for k ,itr in zip(index,triangle_window):
                #     st.write(k, itr)
                for k ,itr in zip(index,triangle_window):
                    # st.write(k)
                    new_mag[k]=new_mag[k]*itr 
                    # st.write(itr)
                    # st.write(k)
        else:
            break            


if 'i' not in st.session_state:
    st.session_state.i = 0

if 'audio' not in st.session_state:
    st.session_state.audio = 0

if 't_sampled' not in st.session_state:
    st.session_state.t_sampled = np.zeros(10)

if 't' not in st.session_state:
    st.session_state.t = np.zeros(10)

if 'signal_sampled' not in st.session_state:
    st.session_state.signal_sampled = np.zeros(10)

if 'freq' not in st.session_state:
    st.session_state.freq = np.zeros(10)

if 'mag' not in st.session_state:
    st.session_state.mag = np.zeros(10)

if 'phase' not in st.session_state:
    st.session_state.phase = np.zeros(10)

if 'audio_dataFrame' not in st.session_state:
    st.session_state.audio_dataFrame = pd.DataFrame({'time' : st.session_state.t_sampled, 'signal' : list(st.session_state.signal_sampled)}, columns = ['time', 'signal'])

if 'edited_audio_dataFrame' not in st.session_state:
    st.session_state.edited_audio_dataFrame = pd.DataFrame({'time' : st.session_state.t_sampled, 'signal' : list(st.session_state.signal_sampled)}, columns = ['time', 'signal'])

# ploting section----------------------------------------------------------------------------------------------

place_holder = st.empty()

col1, col2 = st.columns([1,3])
place_holder = col2


with col1:

    render_svg("assests\logo.svg")
    st.header("Equalizer")
    file = st.file_uploader(label="Upload File", key="uploaded_file",type=["wav"])
    Ncol1, Ncol2 = st.columns([1, 1])
    start_btn = Ncol1.button('Start')
    pause_btn = Ncol2.button('Pause')
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
    .css-11ystmq {{
    background-color: #072a51 !important;
    border-radius: 23px !important;
    padding-bottom: 16px !important;
    }}
    </style>
    """  
    st.markdown(browseButton_style, unsafe_allow_html=True)



with col2:
    # if file is None:
    #     lines = plot_altair(st.session_state.audio_dataFrame, st.session_state.edited_audio_dataFrame, st.session_state.i)
    #     line_plot = st.altair_chart(lines)

    if file is not None:
        place_holder.empty()
        signal, sample_rate =librosa.load(file)
        st.session_state.t=np.array(range(0,len(signal)))/(sample_rate)

        st.session_state.mag, st.session_state.phase, st.session_state.freq = fourier_transform(signal,sample_rate)

        # lines = plot_altair(st.session_state.audio_dataFrame, st.session_state.edited_audio_dataFrame, st.session_state.i)
        # line_plot = st.altair_chart(lines)
        
        pygame.mixer.init()
        pygame.mixer.music.load(file.name)
        
        st.session_state.signal_sampled, st.session_state.t_sampled = sampled_signal(signal, st.session_state.t)

        line_plot, Audio_dataFrame, edited_Audio_dataFrame = plot_init(st.session_state.t_sampled, st.session_state.signal_sampled, st.session_state.signal_sampled)

        f, ax = init_plot()
        add_to_plot(ax,signal,sample_rate)

        st.session_state.audio_dataFrame= pd.DataFrame({'time' : st.session_state.t_sampled, 'signal' : list(st.session_state.signal_sampled)}, columns = ['time', 'signal'])




        # start_btn = st.button("Start", key = start_btn)
        # pause_btn = st.button("Pause", key = pause_btn)   
        



        # with st.expander("Spectogram"): 
        #         show_plot(f)

with st.container():
    col1, gap, col2,gap = st.columns([0.07,0.03,0.07,1])


uniform_tab, vowels_tab, Instruments_tab, Voice_Changer_tab = st.tabs(["Uniform", "Vowels", "Instruments","Voice Changer"])

with uniform_tab:
    
    first_columns=st.columns(10)
    first_counter=0
    first_index = 0
    last_index = 9
    first_list_of_sliders_values = []
    while first_counter < 10:
        with first_columns[first_counter]:
            first_slider = vertical_slider(0,1,-10,5,first_counter)
        first_counter +=1
        first_list_of_sliders_values.append(first_slider) 
    first_index=0
    last_index=9
    drop(first_index, last_index, first_list_of_sliders_values, st.session_state.freq, st.session_state.mag)

with vowels_tab:
    second_columns=st.columns(4)
    second_counter=0
    first_index = 10
    last_index = 13
    second_list_of_sliders_values = []
    while second_counter < 4:
        with second_columns[second_counter]:
            second_sliders_key=second_counter+10
            second_slider = vertical_slider(0,1,-10,5,second_sliders_key)
        second_counter +=1
        second_list_of_sliders_values.append(second_slider)

with Instruments_tab:
    third_columns=st.columns(3)
    third_counter=0
    first_index = 14
    last_index = 16
    third_list_of_sliders_values = []
    while third_counter < 3:
        with third_columns[third_counter]:
            third_sliders_key = third_counter+14
            third_slider = vertical_slider(0,1,-10,5,third_sliders_key)
        third_counter +=1
        third_list_of_sliders_values.append(third_slider)


with Voice_Changer_tab:
    st.header(" ")
    col1, col2 = st.columns([1,1])
    with col1:
        change_to_male_voice = st.button('Male Voice')
    with col2:
        change_to_female_voice = st.button('Female Voice')

if 'state_flag' not in st.session_state:
    st.session_state.state_flag = 0     

if start_btn:
    with col2:
        inv_fourier_signal =  invers(st.session_state.mag, st.session_state.phase)
        sampled_inv, st.session_state.t_sampled = sampled_signal(inv_fourier_signal, st.session_state.t)
        st.session_state.edited_audio_dataFrame= pd.DataFrame({'time' : st.session_state.t_sampled, 'signal' : list(sampled_inv)}, columns = ['time', 'signal'])
        st.session_state.i = 0
        st.session_state.state_flag = 0
        start_Plotting(st.session_state.t_sampled, line_plot, 0.117, st.session_state.audio_dataFrame, st.session_state.edited_audio_dataFrame)


if pause_btn:
    if st.session_state.state_flag == 0:
        pygame.mixer.music.pause()
        st.session_state.state_flag = 1
    else:
        pygame.mixer.music.unpause()
        st.session_state.state_flag = 0
        with col2:
            start_Plotting(st.session_state.t_sampled, line_plot, 0.117, st.session_state.audio_dataFrame, st.session_state.edited_audio_dataFrame)