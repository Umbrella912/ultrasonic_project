import serial
import time
import numpy as np
import matplotlib.pyplot as plt

PORT = 'COM6'
distances_cm = [10, 20, 30]
N = 50

ser = serial.Serial(PORT, 115200, timeout=1)
time.sleep(2)

measured_us = []
for dist_cm in distances_cm:
    expected = dist_cm * 58.31
    while True:
        input('Place the flat target exactly %d cm from the sensor, then press Enter...' % dist_cm)
        ser.reset_input_buffer()
        vals = []
        while len(vals) < N:
            raw = ser.readline().decode(errors='ignore').strip()
            try:
                ms, us = map(int, raw.split(','))
                if us > 0:
                    vals.append(us)
            except ValueError:
                pass
        med = float(np.median(vals))
        print('%d cm -> min %d, median %.1f, max %d, std %.1f us (expected about %.0f us)'
              % (dist_cm, min(vals), med, max(vals), np.std(vals), expected))
        if abs(med - expected) / expected < 0.15 and np.std(vals) < 50:
            break
        again = input('This looks off. Type r to retry, or press Enter to keep it: ')
        if again.strip().lower() != 'r':
            break
    measured_us.append(med)
ser.close()

dist_m = np.array(distances_cm) / 100.0
tau_s = np.array(measured_us) * 1e-6

slope, intercept = np.polyfit(dist_m, tau_s, 1)
v_est = 2 / slope
print('Fitted slope = %.6f s/m' % slope)
print('Estimated speed of sound = %.1f m/s' % v_est)
print('Theoretical (343 m/s) slope = %.6f s/m' % (2 / 343.0))

plt.figure(figsize=(8, 5))
plt.plot(dist_m * 100, tau_s * 1e6, 'o', label='Measured delay')
plt.plot(dist_m * 100, (slope * dist_m + intercept) * 1e6, '-', label='Best-fit line')
plt.plot(dist_m * 100, (2 * dist_m / 343.0) * 1e6, '--', label='Theory (343 m/s)')
plt.xlabel('Distance d (cm)')
plt.ylabel('Echo delay tau (microseconds)')
plt.title('Ultrasonic echo as a delay system')
plt.legend()
plt.grid(True)
plt.savefig('project_c_plot.png', dpi=150)
plt.show()