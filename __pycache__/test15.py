from scipy.io import wavfile
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from scipy.signal import find_peaks
from scipy.fftpack import fft
from scipy.io import wavfile
from fn import _
from scipy.io.wavfile import write


file = st.file_uploader(label="Upload Sound File", key="uploaded_file",type=["wav"])

# def fourier(signal, sampleRate):
#     n_samples = len(signal)
#     f_hat = np.fft.fft(signal, n_samples)
#     l = (len(f_hat))
#     f = f_hat[:l]
#     tpCount     = len(signal)
#     values      = np.arange(int(tpCount))
#     timePeriod  = tpCount/sampleRate 
#     frequencies = values/timePeriod
#     return frequencies, f 

radio_button=st.radio('music')

slider_0=st.slider('jo')
slider_1=st.slider()
slider_2=st.slider()
slider_3=st.slider()


sliders=[slider_0, slider_1, slider_2, slider_3]

def fourier(audio=[], samplfreq=440010):
    try:
        audio=audio[:,1]
    except:
        audio=audio[:]
    fourier_transform_magnitude=np.fft.rfft(audio)
    fourier_transform_freq=np.fft.rfftfreq(len(audio), 1/samplfreq)
    return fourier_transform_magnitude,fourier_transform_freq

if file is not None:
    path=file.name
    samplfreq , audio=wavfile.read(path)
    magnitude , frequencies=fourier(audio, samplfreq)

    points_per_Freq=int(len(frequencies) / (samplfreq/2) )

    numpoints_1=np.abs(0*points_per_Freq - 500*points_per_Freq)
    numpoints_2=np.abs(500*points_per_Freq - 1000*points_per_Freq)
    numpoints_3=np.abs(1000*points_per_Freq - 2000*points_per_Freq)
    numpoints_4=np.abs(20000*points_per_Freq - 5000*points_per_Freq)
    startindex_1=0*points_per_Freq
    print(5000*points_per_Freq)
    startindex_2=500*points_per_Freq
    startindex_3=1000*points_per_Freq
    startindex_4=2000*points_per_Freq

if radio_button=='music' and len(magnitude)>10:
    magnitude=modify_wave(magnitude,numpoints_1,startindex_1,sliders[0]*10)
    magnitude=modify_wave(magnitude,numpoints_2,startindex_2,sliders[1]*10)
    magnitude=modify_wave(magnitude,numpoints_3,startindex_3,sliders[2]*10)
    magnitude=modify_wave(magnitude,numpoints_4,startindex_4,sliders[3]*10)

    new_sig=np.fft.irfft(magnitude)
    norm_new_sig=np.int16(new_sig*(1367736/new_sig.max()))
    write('convertwave.wav',samplfreq,norm_new_sig)
    st.audio('convertwave.wav')