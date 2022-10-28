import numpy as np
from scipy.io import wavfile
import base64
import streamlit as st
import pandas as pd
import wave

def read_wav(file):
    spf = wave.open(file, "r")
    return spf