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
    slider_value = _vertical_slider(value=value,step=step, min=min, max=max, key=key, default=value)
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
def plot_altair(df, cutoff):
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
    end = math.ceil(df["time"].iloc[-1])
    base = alt.Chart(df).mark_rule().encode(
            x=alt.X('time', axis=alt.Axis(title='Time'), scale=alt.Scale(domain=(0, end))),
            y=alt.Y('signal', axis=None),
            color = alt.condition(alt.datum["time"] < selector["cutoff"],
        alt.value("#1F618D"),
        alt.value("#BBDEFB")),
        
    ).properties(
            width=1300,
            height=200
    ).add_selection(
            selector,
            zoom,
            selection
    )
 
    base1 = alt.Chart(df).mark_rule().encode(
            x=alt.X('time', axis=alt.Axis(title='Time'), scale=alt.Scale(domain=(0, end))),
            y=alt.Y('signal', axis=None),
            color = alt.condition(alt.datum["time"] < selector["cutoff"],
        alt.value("#1F618D"),
        alt.value("#BBDEFB")),
        
    ).properties(
            width=1300,
            height=200
        ).add_selection(
            selector,
            zoom,
            selection
        )
    chart1=base.encode()
    chart2=base1.encode()
    figure = alt.vconcat(chart1, chart2).configure_axis(
        gridColor = '#D6EAF8',
        domainColor = 'white',
    )
    return figure


# ---------------------------------------------------------------------------------------------------
def start_Plotting (time, line_plot, step):
    pygame.mixer.init()
    pygame.mixer.music.play(start= st.session_state.i)     
    for st.session_state.i in np.arange(st.session_state.i, math.ceil(time[-1]), step): # asyncronous timing
        lines = plot_altair(df, st.session_state.i)
        line_plot = line_plot.altair_chart(lines)
     

if 'i' not in st.session_state:
    st.session_state.i = 0

if 'audio' not in st.session_state:
    st.session_state.audio = 0

# ploting section----------------------------------------------------------------------------------------------


col1, col2 = st.columns([1,3])


with col1:

    render_svg("assests\logo.svg")
    st.header("Equalizer")
    file = st.file_uploader(label="Upload File", key="uploaded_file",type=["wav"])
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

    if file is not None:

        x, sr =librosa.load(file)
        t=np.array(range(0,len(x)))/(sr)

        pygame.mixer.init()
        pygame.mixer.music.load(file.name)
        
        x_, t_ = sampled_signal(x, t)
        f, ax = init_plot()
        add_to_plot(ax,x,sr)
        df = pd.DataFrame({'time' : t_, 'signal' : list(x_)}, columns = ['time', 'signal'])

        lines = plot_altair(df, st.session_state.i)
        line_plot = st.altair_chart(lines)


        start_btn = st.button("Start" )
        pause_btn = st.button("Pause")
        resume_btn = st.button("resume")    
        
        if start_btn:

            st.session_state.i = 0
            
            
            start_Plotting(t_, line_plot, 0.117)
        

        if pause_btn:
            pygame.mixer.music.pause()
        
        if resume_btn:
        
            pygame.mixer.music.unpause()
            start_Plotting(t_, line_plot, 0.117)

        with st.expander("Spectogram"): 

                show_plot(f)

with st.container():
    col1, gap, col2,gap = st.columns([0.07,0.03,0.07,1])
    start_btn = col1.button('Start')
    pause_btn = col2.button('Pause')


tab1, tab2, tab3, tab4 = st.tabs(["Uniform", "Vowels", "Instruments","Voice_Changer"])

with tab1:

    first_columns=st.columns(10)
    first_counter=0
    first_list_of_sliders_values = []
    while first_counter < 10:
        with first_columns[first_counter]:
            first_slider = vertical_slider(5,1,0,5,first_counter)
        first_counter +=1
        first_list_of_sliders_values.append(first_slider) 
    

with tab2:
    second_columns=st.columns(4)
    second_counter=0
    second_list_of_sliders_values = []
    while second_counter < 4:
        with second_columns[second_counter]:
            second_sliders_key=second_counter+10
            second_slider = vertical_slider(2,1,0,5,second_sliders_key)
        second_counter +=1
        second_list_of_sliders_values.append(second_slider)


with tab3:
    third_columns=st.columns(3)
    third_counter=0
    third_list_of_sliders_values = []
    while third_counter < 3:
        with third_columns[third_counter]:
            third_sliders_key = third_counter+14
            third_slider = vertical_slider(2,1,0,5,third_sliders_key)
        third_counter +=1
        third_list_of_sliders_values.append(third_slider)


with tab4:
    change_to_male_voice = st.checkbox('Male Voice')
    change_to_female_voice = st.checkbox('Female Voice')
