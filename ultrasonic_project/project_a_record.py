import serial
import time
import numpy as np
import matplotlib.pyplot as plt

PORT = 'COM6'   # change to your port
DURATION = 20

ser = serial.Serial(PORT, 115200, timeout=1)
time.sleep(2)
ser.reset_input_buffer()

rows = []
t0 = time.time()
while time.time() - t0 < DURATION:
    raw = ser.readline().decode(errors='ignore').strip()
    try:
        ms, us = map(int, raw.split(','))
        if us > 0:
            rows.append((ms, us))
    except ValueError:
        pass
ser.close()

data = np.array(rows)
t = (data[:, 0] - data[0, 0]) / 1000.0
dist = data[:, 1] * 0.0343 / 2

Ts = np.mean(np.diff(t))
print('Samples recorded:', len(t))
print('Average sampling period Ts = %.3f s' % Ts)
print('Sampling frequency fs = %.1f Hz' % (1 / Ts))
print('Nyquist frequency = %.1f Hz' % (1 / (2 * Ts)))

np.savetxt('project_a_data.csv', np.column_stack((t, dist)),
           delimiter=',', header='time_s,distance_cm', comments='')

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 6))
ax1.plot(t, dist)
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Distance (cm)')
ax1.set_title('Recorded distance signal x[n]')

ax2.stem(t[:60], dist[:60])
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Distance (cm)')
ax2.set_title('First 60 samples (discrete-time view)')

plt.tight_layout()
plt.savefig('project_a_plot.png', dpi=150)
plt.show()