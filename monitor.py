import datetime
import time
import serial
import pandas as pd
import matplotlib.pyplot as plt
from math import floor

ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600)

df = pd.DataFrame(columns=['t', 'T'])

today = datetime.date.today()

try:
    df = pd.read_csv("{}.csv".format(str(today)), names=["t", "T"])
except:
    df = pd.DataFrame()

fig, ax = plt.subplots(1,1, figsize=(4, 2))
plt.ion()
plt.show()

bold_text = 0

while True:
    T_k = float(ser.readline())
    t_k = datetime.datetime.now().replace(microsecond=0)#.isoformat()
    dt = datetime.timedelta(minutes=20)

    if bold_text == 0 and floor(T_k) % 5 == 0:
        bold_text = 30

    row_k = {'t': pd.to_datetime(t_k), 'T': T_k}
    df = df.append(row_k, ignore_index=True)

    ax.clear()

    ax.set_xlim([t_k - dt, t_k])
    ax.scatter(df["t"], df["T"])
    ax.set_ylim(15, df["T"].max() * 1.5)
    ax.grid()

    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature")

    ax.set_title("Current temperature: {}".format(T_k))

    if bold_text > 0:
        props = dict(boxstyle='round', facecolor='red', alpha=0.5)
        ax.text(0.05, 0.95, "Temperature is {}".format(T_k),
            transform=ax.transAxes, fontsize=14,
            verticalalignment='top', bbox=props)
        bold_text -= 1

    # Update plot
    plt.draw()
    plt.pause(1)


    with open("{}.csv".format(str(today)), "a") as f:
        f.write("{},{}\n".format(t_k, T_k))

    