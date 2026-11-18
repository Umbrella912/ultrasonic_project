import serial
import time
from collections import deque
import matplotlib.pyplot as plt

PORT = 'COM6'   # change to your port

ser = serial.Serial(PORT, 115200, timeout=1)
time.sleep(2)

times = deque(maxlen=300)
dists = deque(maxlen=300)

plt.ion()
fig, ax = plt.subplots()
line, = ax.plot([], [], 'o-')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Distance (cm)')
ax.set_title('Ultrasonic distance signal')
ax.set_ylim(0, 200)

start = None
while plt.fignum_exists(fig.number):
    raw = ser.readline().decode(errors='ignore').strip()
    try:
        ms, us = map(int, raw.split(','))
    except ValueError:
        continue
    if us == 0:
        continue
    if start is None:
        start = ms
    times.append((ms - start) / 1000.0)
    dists.append(us * 0.0343 / 2)
    line.set_data(times, dists)
    ax.set_xlim(max(0, times[-1] - 10), max(10, times[-1]))
    plt.pause(0.001)

ser.close()