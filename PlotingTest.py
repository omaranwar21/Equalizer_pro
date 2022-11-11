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
import matplotlib.pyplot as plt
# import schedule

st.set_page_config(
    page_title="Equalizer",
    page_icon="🔉",
    layout="wide"
)

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

    

if 'i' not in st.session_state:
    st.session_state.i = 0


x, sr =librosa.load(r"C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\Media\\S1 (mp3cut.net).wav")
t=np.array(range(0,len(x)))/(sr)
x_, t_ = sampled_signal(x, t)
df = pd.DataFrame({'time' : t_, 'signal' : list(x_)}, columns = ['time', 'signal'])
lines = plot_altair(df, st.session_state.i)
line_plot = st.altair_chart(lines)

with st.container():
    col1,gap,col2 = st.columns([1,1,1])
    start_btn = col1.button('Start')
    pause_btn = col2.button('Pause')

    if 'maxi' not in st.session_state:
        st.session_state.maxi = math.ceil(t_[-1])


    if start_btn:
        # timer = 0.0001
        # timer = start_Plotting(t_, line_plot, timer)
        start_Plotting(t_, line_plot, 0.07)




    value = math.ceil(st.session_state.i)
    if value == st.session_state.maxi:
        st.session_state.i = 0
        start_Plotting(t_,line_plot, 0.07)



    view_spec = col1.button('view')
    
    if view_spec:
        fig, ax = plt.figure(figsize=(9, 3))

        # plt.xlabel('Time')

        # plt.ylabel('Frequency')
        ax.specgram(x,Fs=sr)
        st.pyplot(fig)

    # HtmlFile = open("index.html", 'r', encoding='utf-8')
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
    #   <source src="../Media/S1(mp3cut.net).wav" type="audio/wav">
    #   <source src="../Media/S1(mp3cut.net).wav" type="audio/wav">
    #   Your browser does not support the audio element.
    # </audio>

    # <p>Click the buttons to play or pause the audio.</p>

    # <button onclick="playAudio()" type="button">Play Audio</button>
    # <button onclick="pauseAudio()" type="button">Pause Audio</button> 
    # """

    # my_comp = f"<script>{my_js}</script>"

    # sound = st.empty()            
    # sound.markdown(html_string, unsafe_allow_html=True)
    # html(html_string)
    # html(my_comp)

    # st.audio("C:\\Users\\Anwar\\Desktop\\SBME 2024\\YEAR 3 (2022-2023)\\DSP\\Tasks\\Task 2\\DSP_Task2\\Media\\S1 (mp3cut.net).wav")
    st.write(ipd.Audio(x, rate=sr, autoplay = True))
