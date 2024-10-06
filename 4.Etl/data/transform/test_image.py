import numpy as np
import matplotlib.pyplot as plt
from obspy import read
from scipy.fft import fft, fftfreq
import pywt  # For wavelet transform

# Function to plot the Fourier Transform
def plot_fourier_transform(data, sampling_rate, title):
    # Compute the Fourier Transform
    N = len(data)
    T = 1.0 / sampling_rate
    yf = fft(data)
    xf = fftfreq(N, T)[:N // 2]

    # Plot the result
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    plt.plot(xf, 2.0 / N * np.abs(yf[:N // 2]), color='red')
    plt.title(f'Fourier Transform - {title}', color='white')
    plt.xlabel('Frequency (Hz)', color='white')
    plt.ylabel('Amplitude', color='white')
    plt.grid(True, linestyle='--', color='gray')
    plt.show()

# Function to plot the Continuous Wavelet Transform (CWT)
def plot_wavelet_transform(data, sampling_rate, title):
    # Perform Continuous Wavelet Transform (CWT) using 'cmor' wavelet (complex morlet)
    scales = np.arange(1, 128)
    wavelet = 'cmor'
    coef, freqs = pywt.cwt(data, scales, wavelet, 1.0 / sampling_rate)

    # Plot the result as a scalogram
    plt.figure(figsize=(10, 6))
    plt.style.use('dark_background')
    plt.imshow(np.abs(coef), extent=[0, len(data) / sampling_rate, freqs[-1], freqs[0]], cmap='inferno', aspect='auto')
    plt.colorbar(label='Magnitude')
    plt.title(f'Wavelet Transform (Scalogram) - {title}', color='white')
    plt.xlabel('Time (seconds)', color='white')
    plt.ylabel('Frequency (Hz)', color='white')
    plt.grid(False)
    plt.show()

# Load the seismic data
mseed_file = 'space_apps_2024_seismic_detection/data/moon/test/data/S12_GradeB/xa.s12.00.mhz.1969-12-16HR00_evid00006.mseed'  # Replace with the actual path
st = read(mseed_file)
sampling_rate = st[0].stats.sampling_rate  # Sampling rate of the data
original_signal = st[0].data

# Plot Fourier Transform of the original signal
plot_fourier_transform(original_signal, sampling_rate, 'Original Signal')

# Plot Wavelet Transform (Scalogram) of the original signal
plot_wavelet_transform(original_signal, sampling_rate, 'Original Signal')