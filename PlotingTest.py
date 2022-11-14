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
# import simpleaudio as sa
# import aud

# import schedule

st.set_page_config(
    page_title="Equalizer",
    page_icon="🔉",
    layout="wide"
)

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
# @st.cache (suppress_st_warning = True, persist = False, show_spinner = False, allow_output_mutation=True)
def add_to_plot(ax,x,sr):
  ax.specgram(x,Fs = sr)  # alpha represent the brightness of the line

#fuction to shaw the plotting
def show_plot(f):
        st.pyplot(f)   

def sampled_signal(signal, time):
    pack = 100
    sampled_time= time[::pack]
    sampled_signal= signal[::pack]
    return sampled_signal, sampled_time
# alt.renderers.enable('altair_viewer')

def plot_altair(df, cutoff):
    # x_, t_ = sampled_signal(x,y)
    # df = pd.DataFrame({'time' : t_, 'signal' : list(x_)}, columns = ['time', 'signal'])
    # pack = 700
    # i = 0
    # while(pack+1 != len(x_)):
    # x = 'time'[i:pack+i:pack]
    # y = 'signal'[i:pack+i:pack]
    # st.write(df["time"].iloc[-1])
    # slider = alt.binding_range(
    # min=df["time"].min(),
    # max=df["time"].max(),
    # step=0.5,
    # name="time",
    # )
    zoom = alt.selection_interval(
    bind='scales',
    # bind_y = False,
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
        # bind=slider,
        init={"cutoff": cutoff},
    )
    end = math.ceil(df["time"].iloc[-1])
    # brush = alt.selection_interval(encodings=['x'])
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
            # brush
    )
    # end = math.ceil(df["time"].iloc[-1])
    # brush = alt.selection_interval(encodings=['x'])
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
    # st.altair_chart(base, use_container_width=True)
    chart1=base.encode()
    chart2=base1.encode()
    figure = alt.vconcat(chart1, chart2).configure_axis(
        gridColor = '#D6EAF8',
        # grid=False,
        # disable = True,
        domainColor = 'white',
        # domainOpacity = 0,
    )
    return figure


# def plot_animation(df, first, second):
#     brush = alt.selection_interval()
#     chart1 = alt.Chart(df).mark_line().encode(
#             x=alt.X('time', axis=alt.Axis(title='Time') , scale=alt.Scale(domain=(first, second))),
#             y=alt.Y('signal', axis=alt.Axis(title='Amplitude')),
#         ).properties(
#             width=1000,
#             height=50
#         ).add_selection(
#             brush
#         ).interactive()
    
#     figure = chart1.encode(y=alt.Y('signal',axis=alt.Axis(title='Amplitude')))
#     #  | chart1.encode(y ='amplitude after processing').add_selection(
#     #         brush)
#     return figure 

def start_Plotting (time, line_plot, step):
    # program_starts = time.time()
    for st.session_state.i in np.arange(st.session_state.i, math.ceil(time[-1]), step): # asyncronous timing
        lines = plot_altair(df, st.session_state.i)
        line_plot = line_plot.altair_chart(lines)
        # now = time.time()
        # timer = now - program_starts
    # return timer   

# def convert_to_mp3 (wav_file):
#     sound = pydub.AudioSegment.from_wav(wav_file)
#     mp3_file = os.path.splitext(wav_file)[0] + '.mp3'
#     sound.export(mp3_file, format="mp3")
#     return 

    

if 'i' not in st.session_state:
    st.session_state.i = 0

if 'audio' not in st.session_state:
    st.session_state.audio = 0


x, sr =librosa.load(r"C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\g_sentence.wav")
# source = audio. play_file("g_sentence.wav")
# playback = Playback() # creates an object for managing playback of a single audio file
# playback.load_file("C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\g_sentence.mp3")
# sound = pydub.AudioSegment.from_wav("C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\Media\\S1(mp3cut.net).wav")

# sound.export("C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\Media\\S1(mp3cut.net).mp3", format="mp3")
# x, sr =librosa.load(r"C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\g_sentence.wav")


# root = r'g_sentence.wav'

# x, sr = librosa.load(root)

# x_fast = librosa.effects.time_stretch(x, rate=1.5)
# Audio(x_fast, rate = sr)

pygame.mixer.init()

# sound = AudioSegment.from_file(root)

# so = sound.speedup(1.5, 300, 25)

# so.export(root[:-4] + '_down.wav', format = 'wav')

pygame.mixer.music.load("C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\g_sentence.wav")
# wave_obj = sa.WaveObject.from_wave_file("g_sentence.wav")


# x, sr = librosa.load(root)


t=np.array(range(0,len(x)))/(sr)

x_, t_ = sampled_signal(x, t)
f, ax = init_plot()

add_to_plot(ax,x,sr)
df = pd.DataFrame({'time' : t_, 'signal' : list(x_)}, columns = ['time', 'signal'])

lines = plot_altair(df, st.session_state.i)
line_plot = st.altair_chart(lines)

with st.container():
    col1,gap,col2,gap, col3 = st.columns([1,1,1,1,1])
    start_btn = col1.button('Start')
    pause_btn = col2.button('Pause')
    resume_btn = col3.button('resume')

    # if 'maxi' not in st.session_state:
    #     st.session_state.maxi = math.ceil(t_[-1])


    # view_spec = col1.button('view')

    if start_btn:

        # if st.session_state.i == 0:
        st.session_state.i = 0
        # audio. play_file("g_sentence.wav")
        # play_obj = wave_obj.play()
        pygame.mixer.music.play()        
        # st.write(ipd.Audio(x,rate=sr,autoplay=True))
        # pygame.mixer.music.play()
        # pygame.mixer.music.set_pos(st.session_state.i/1000.0)
        # playback.play()
        # else:
        # st.session_state.i = 0
        # st.empty().write(ipd.Audio(x, rate=sr, autoplay = True))
        start_Plotting(t_, line_plot, 0.117)
        # st.empty().empty()
        # timer = 0.0001
        # timer = start_Plotting(t_, line_plot, timer)

    if pause_btn:
        # source.set_paused(True)
        pygame.mixer.music.pause()
        # play_obj.pause()
        # start_Plotting(t_, line_plot, 0.117)
        # playback.pause()

    if resume_btn:
        # source.set_paused(True)
        # st.write(st.session_state.i)
        # pygame.mixer.music.play()
        # playback.seek(st.session_state.i)
        # pygame.mixer.music.set_pos(st.session_state.i/1000.0)
        pygame.mixer.music.unpause()
        # play_obj.resume()
        start_Plotting(t_, line_plot, 0.117)

    # value = math.ceil(st.session_state.i)
    # if value == st.session_state.maxi:
    #     st.session_state.i = 0
    #     start_Plotting(t_,line_plot, 0.07)

    # view_flag = 0
    # if view_spec:
    with st.expander("Spectogram"): 
    #     if view_flag == 0:
    #         view_flag = 1
            show_plot(f)
    #     else:
    #         view_flag = 0
    #         ax.clf()

    
    
        # fig, ax = plt.figure(figsize=(9, 3))

        # plt.xlabel('Time')

        # plt.ylabel('Frequency')
        # ax.specgram(x,Fs=sr)
        # st.pyplot(fig)

    # HtmlFile = open("index.html", 'r', encoding='utf-8')
    # path_to_audio = "/Media/S1(mp3cut.net).wav"
    # audio_type = "wav"

    # my_js = """
    # var x = document.getElementById("myAudio"); 

    # function playAudio() { 
    #   x.play(); 
    # } 

    # function pauseAudio() { 
    #   x.pause(); 
    # } 
    # """

    # html_string = """
    #             <audio id="myAudio">
    #   <source src="..{0}" type="audio/{1}">
    #   <source src="..{0}" type="audio/{1}">
    #   Your browser does not support the audio element.
    # </audio>

    # <p>Click the buttons to play or pause the audio.</p>

    # <button onclick="playAudio()" type="button">Play Audio</button>
    # <button onclick="pauseAudio()" type="button">Pause Audio</button> 
    # """.format(path_to_audio, audio_type)

    # my_comp = f"<script>{my_js}</script>"

    # # sound = st.empty()            
    # # sound.markdown(html_string, unsafe_allow_html=True)
    # html(html_string)
    # html(my_comp)

    # st.audio("C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\Media\\S1 (mp3cut.net).wav")
