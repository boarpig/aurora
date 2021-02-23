#!/usr/bin/python3
import requests
import matplotlib.pyplot as plt
import json
import numpy as np
from matplotlib import dates as mdates
from datetime import datetime

dataurl = "https://cdn.fmi.fi/apps/magnetic-disturbance-observation-graphs/serve-data.php"
r = requests.get(dataurl)

data = r.json()
times = []
points = []
for time, point in data["SOD"]["dataSeries"]:
    times.append(time / 1000)
    if point:
        points.append(float(point))
    else:
        points.append(0.0)

points = np.array(points)
times = mdates.epoch2num(times)

ax = plt.axes()

formatter = mdates.DateFormatter("%H:%M")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.HourLocator(interval=3)
ax.xaxis.set_major_locator(locator)

minor_formatter = mdates.DateFormatter("%m-%d")
ax.xaxis.set_minor_formatter(minor_formatter)
minor_locator = mdates.DayLocator()
ax.xaxis.set_minor_locator(minor_locator)

ax.xaxis.set_tick_params(which='minor', pad=15)

colormap = np.where(points>0.5, 'r', 'b')
plt.ylim(0, 1)
plt.axhline(0.5)
plt.bar(times, points, color=colormap, width=0.005)

for tick in plt.xticks()[0]:
    plt.axvline(tick, dashes=(1,2), linewidth=0.5)

ax.set_ylabel('nT/s')
ax.set_title("Magneettinen aktiivisuus kuluneen vuorokauden aikana")

fig = plt.figure(1)
fig.set_size_inches(15, 5)

plt.show()
#plt.savefig("figure.png")
