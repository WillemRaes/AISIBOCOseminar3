import numpy as np
from scipy import signal
import matplotlib.pyplot as plt



def square_wave_corr(spectrum, N, m):
    corr_function = np.multiply(np.divide(np.sin(np.pi * m / N) * N, m * np.pi), np.exp(-1j * m * np.pi / N))

    corr_spec = np.multiply(spectrum, corr_function)

    return corr_spec


np.set_printoptions(threshold=np.inf)

fs = 51200.0 * 2
f1 = 400.0
N = 256
T = 1.0 / (fs)
A = 1.0
d = 0.5

fd1 = f1 / fs

t = np.linspace(0, N - 1, N, endpoint=True)
m = np.linspace(0, N - 1, N, endpoint=True)
# t2= np.linspace(0, N-1, N, endpoint = True)


sig1 = (1 + signal.square(2 * np.pi * fd1 * t, d)) * 0.5
sig2 = (1 + signal.square(2 * np.pi * fd1 * 2 * t, d)) * 0.5
sig3 = (1 + signal.square(2 * np.pi * fd1 * 3 * t, d)) * 0.5
sig4 = (1 + signal.square(2 * np.pi * fd1 * 4 * t, d)) * 0.5
plt.figure(1)
plt.subplot(311)
plt.plot(t, sig1)

Cn1 = np.fft.fftshift(np.fft.fft(sig1)) / float(N)
Cn2 = np.fft.fftshift(np.fft.fft(sig2)) / float(N)
Cn3 = np.fft.fftshift(np.fft.fft(sig3)) / float(N)
Cn4 = np.fft.fftshift(np.fft.fft(sig4)) / float(N)
Cn_t = np.fft.fftshift(np.fft.fft(sig1 + sig2 + sig3 + sig4)) / float(N)

spectrum1 = Cn1[int(N / 2 + 1):]
spectrum2 = Cn2[int(N / 2 + 1):]
spectrum3 = Cn3[int(N / 2 + 1):]
spectrum4 = Cn4[int(N / 2 + 1):]

spectrum_t = Cn_t[int(N / 2 + 1):]

m = m[1:int(N / 2)]

# corr_spectrum= square_wave_corr(spectrum1, N, m)

# corr_spectrum_t = square_wave_corr(spectrum_t, N, m)
FR1 = np.abs(spectrum1)
FR2 = np.abs(spectrum2)
FR3 = np.abs(spectrum3)
FR4 = np.abs(spectrum4)
FR_t = np.abs(spectrum_t)

# FR_corr=np.abs(corr_spectrum)

FR_corr_t = np.abs(spectrum_t)

plt.subplot(312)
plt.xlim(0, 30)
plt.stem(m, FR1)
plt.stem(m, FR2, 'r')
plt.stem(m, FR3, 'g')
plt.stem(m, FR4, 'b')

plt.subplot(313)
plt.xlim(0, 30)
plt.stem(m, FR_corr_t)
plt.show()

diff = FR_t - FR_corr_t
print("FR", FR_t)
print("FR_Corr", FR_corr_t)

print("Difference", diff)