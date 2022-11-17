# plot in real time with x-axis
# import numpy as np
# import matplotlib.pyplot as plt

# # Initialize
# x_axis_start = 0
# x_axis_end = 10

# plt.axis([x_axis_start, x_axis_end, 0, 1])
# plt.ion()

# # Realtime plot
# for i in range(200):
#     y = np.random.random()
#     plt.scatter(i, y)
#     plt.pause(0.00001)

#     if i%10 == 0 and i>1:
#         print("Axis should update now!")
#         x_axis_start += 5
#         x_axis_end += 10
#         plt.axis([x_axis_start, x_axis_end, 0, 1])




#animate the graph--------------------------------------------------------------------
# import pandas as pd
# import numpy as np
# import plotly.express as px
# import plotly.graph_objects as go

# df = pd.DataFrame(
#     {
#         "time": np.tile(pd.date_range("1-jan-2021", freq="1H", periods=12), 10),
#         "x": np.random.uniform(1, 4, 120),
#         "y": np.random.uniform(2, 5, 120),
#     }
# )
# fig = px.scatter(df, x="x", y="y", animation_frame=df["time"].dt.strftime("%H:%M"))

# go.Figure(
#     data=fig.data,
#     frames=[
#         fr.update(
#             layout={
#                 "xaxis": {"range": [min(fr.data[0].x) - 0.1, max(fr.data[0].x) + 0.1]},
#                 "yaxis": {"range": [min(fr.data[0].y) - 0.1, max(fr.data[0].y) + 0.1]},
#             }
#         )
#         for fr in fig.frames
#     ],
#     layout=fig.layout,
# )

# fig.show()

#---------------------------------------------------------------------------------------

from os import path
from pydub import AudioSegment
import ffmpeg

# files                                                                         
src = "half.wav"
dst = "testAudio.mp3"

# convert wav to mp3                                                            
sound = AudioSegment.from_wav(src)
sound.export(dst, format="mp3")
