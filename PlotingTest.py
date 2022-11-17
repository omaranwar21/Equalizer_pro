import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import librosa
import librosa.display
import math
import time
import IPython.display as ipd
from IPython.display import Audio
import streamlit.components.v1 as components
from streamlit.components.v1 import html
from scipy.fft import rfft,irfft, rfftfreq
import matplotlib.pyplot as plt
import pygame
from pydub import AudioSegment
from just_playback import Playback
from replit import audio
import scipy.signal
from os import path
from pydub import AudioSegment
import ffmpeg
from scipy.io.wavfile import write
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
  ax.set_xlabel('Time')                       # the x_axis title
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

def plot_altair(firstDataFrame, secondDataframe, cutoff):

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
            width=1300,
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
            width=1300,
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

    
def start_Plotting (time, line_plot, step,df, df1):
    for st.session_state.i in np.arange(st.session_state.i, math.ceil(time[-1]), step): # asyncronous timing
        lines = plot_altair(df, df1, st.session_state.i)
        line_plot = line_plot.altair_chart(lines)

# def convert_to_mp3 (wav_file):
#     sound = pydub.AudioSegment.from_wav(wav_file)
#     mp3_file = os.path.splitext(wav_file)[0] + '.mp3'
#     sound.export(mp3_file, format="mp3")
#     return 

    

if 'i' not in st.session_state:
    st.session_state.i = 0

if 'audio' not in st.session_state:
    st.session_state.audio = 0

file = "g_sentence(mp3).mp3"
x, sr =librosa.load(file)
y, sr =librosa.load(file)

st.slider('10k', min_value = -5, max_value=5, value=0, step=1, format='%ddb', key= 'slider_value')
# st.writ

def fourier_transform(signal,sr):
    y_sig= scipy.fft.rfft(signal)
    mag=np.abs(y_sig)
    phase=np.angle(y_sig)
    freq= rfftfreq(len(signal),1/sr)
    return mag,phase,freq

ranges1=[[0,5000]]

new_mag=mag.copy()  

def drop(slider_ranges,factor_slider, freq, new_mag):
    for range in slider_ranges:
        index=np.where((freq>range[0])&(freq<range[1]))
        
        
        # triangle_window=10**(factor_slider*scipy.signal.windows.triang(len(index)))
        triangle_window=10**(factor_slider*np.hanning(len(index)))
        # triangle_window=(factor_slider*np.hanning(len(index)))

        for i ,itr in zip(index,triangle_window):
            new_mag[i]=new_mag[i]*itr
        # for i in index:
        #     for (index,iter) in zip(index, triangle_window):
        #         new_mag[i]=new_mag[i]*triangle_window[iter]
            

            # print(i)

drop(ranges1, st.session_state.slider_value, freq, new_mag)

def invers (new_mag,phase):
    y2=np.multiply(new_mag,np.exp(1j*phase))
    inv_fourier_signal = np.real(scipy.fft.irfft(y2))
    return inv_fourier_signal


   

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
# dst = "g_sentence(mp3).mp3"

# # convert wav to mp3                                                            
# sound = AudioSegment.from_wav(file)

t=np.array(range(0,len(x)))/(sr)
# sound.export(dst, format="mp3")
# pygame.mixer.quit()
# clock = pygame.time.Clock()
# mp3 = mutagen.mp3.MP3(file)
# sound = np.array(np.column_stack((t, signalmp3back)), dtype="int8")
# save = "youssef22.mp3"
# write(save,sr, signalmp3back.astype(np.float32))
# pygame.sndarray.make_sound(sound)
# pygame.mixer.init()
# pygame.mixer.music.load(save)

# sound = AudioSegment.from_file(root)

# so = sound.speedup(1.5, 300, 25)

# so.export(root[:-4] + '_down.wav', format = 'wav')


# wave_obj = sa.WaveObject.from_wave_file("g_sentence.wav")


# x, sr = librosa.load(root)






if 'stretched' not in st.session_state:
    st.session_state.stretched = np.zeros(10)

# def callback():



# st.session_state.stretched = librosa.effects.time_stretch(x, rate = float(st.session_state.control_speed[:-1:]))
# # place_holder = st.empty()
# st.write(ipd.Audio(st.session_state.stretched, rate=sr))

# stretch = st.select_slider(
#     'Speed',
#     options=['0.25x', '0.5x', '0.75x', '1x', '1.5x', '1.75x', '2x'],
#     value= '2x',
#     key = 'control_speed',
#     # on_change = callback
#     )

# src = "half.wav"

# # place_holder.empty()
# # st.session_state.control_speed = float(rate_stretch[:-1:]) 
# st.write(st.session_state.control_speed)


f, ax = init_plot()

add_to_plot(ax,x,sr)
def plot_init(t_, x_, y_):
    df = pd.DataFrame({'time' : t_, 'signal' : list(x_)}, columns = ['time', 'signal'])
    df1 = pd.DataFrame({'time' : t_, 'signal' : list(y_)}, columns = ['time', 'signal'])
    lines = plot_altair(df, df1, st.session_state.i)
    line_plot = st.altair_chart(lines)
    return line_plot, df, df1

with st.container():
    col1, gap, col2,gap, col3 = st.columns([0.07, 0.03, 0.07, 1, 1])
    start_btn = col1.button('Start') 
    pause_btn = col2.button('Pause')

    resume_btn = col3.button('resume')

    # if 'maxi' not in st.session_state:
    #     st.session_state.maxi = math.ceil(t_[-1])


    # view_spec = col1.button('view')

    if start_btn:

        # if st.session_state.i == 0:
        signalmp3back = invers(new_mag, phase) 
        x_, t_ = sampled_signal(x, t)
        y_, t_ = sampled_signal(signalmp3back, t)

        line_plot, df, df1 = plot_init(t_,x_,y_)

        st.session_state.i = 0
        place_holder = st.empty()
        st.write(ipd.Audio(signalmp3back,rate=sr))
        # place_holder =  st.audio(file, format ='audio/wav', start_time= int(st.session_state.i))
        # audio. play_file("g_sentence.wav")
        # play_obj = wave_obj.play()
        # pygame.mixer.music.play()        
        # st.write(ipd.Audio(x,rate=sr,autoplay=True))
        # pygame.mixer.music.play()
        # pygame.mixer.music.set_pos(st.session_state.i/1000.0)
        # playback.play()
        # else:
        # st.session_state.i = 0
        # st.empty().write(ipd.Audio(x, rate=sr, autoplay = True))
        start_Plotting(t_, line_plot, 0.117, df, df1)
        # st.empty().empty()
        # timer = 0.0001
        # timer = start_Plotting(t_, line_plot, timer)

    # if pause_btn:
        # place_holder.empty()
        # source.set_paused(True)
        # pygame.mixer.music.pause()
        # play_obj.pause()
        # start_Plotting(t_, line_plot, 0.117)
        # playback.pause()

    if resume_btn:
        # source.set_paused(True)
        # st.write(st.session_state.i)
        # pygame.mixer.music.play()
        # playback.seek(st.session_state.i)
        # pygame.mixer.music.set_pos(st.session_state.i/1000.0)
        # pygame.mixer.music.play(start=st.session_state.i)
        # place_holder =  st.audio(file, format ='audio/wav', start_time= int(st.session_state.i))
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
