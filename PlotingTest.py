import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
from vega_datasets import data

# alt.renderers.enable('altair_viewer')

weather = data.seattle_weather()
car = data.seattle_weather()

x = [weather, car]

base = alt.Chart(car).mark_rule().encode(
    x='date:T',
    y='temp_min:Q',
    y2='temp_max:Q',
    color='weather:N',
    # row=alt.Row("a:N", title="Factor A", header=alt.base)
).interactive()

base1 = alt.Chart(car).mark_rule().encode(
    x='date:T',
    y='temp_min:Q',
    y2='temp_max:Q',
    color='weather:N',
    # row=alt.Row("a:N", title="Factor A", header=alt.base)
).interactive()

# base.encode(y=alt.base) | base.encode(y=alt.base)

st.altair_chart(base | base1, use_container_width=True)