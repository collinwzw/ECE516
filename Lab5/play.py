import pyaudio
import numpy as np
import pylab

import wave
import matplotlib.pyplot as plt

f,ax = plt.subplots(2)
x = np.arange(10000)
y = np.random.randn(10000)
li, = ax[0].plot(x, y)

# Plot 0 is for raw audio data
li, = ax[0].plot(x, y)
ax[0].set_xlim(0,1000)
ax[0].set_ylim(-5000,5000)
ax[0].set_title("Raw Audio Signal")
# Plot 1 is for the FFT of the audio
li2, = ax[1].plot(x, y)
ax[1].set_xlim(0,50)
ax[1].set_ylim(-10,10)
ax[1].set_title("Fast Fourier Transform")
# Show the plot, but without blocking updates
plt.pause(0.01)
plt.tight_layout()

global keep_going
keep_going = True


def plot_data(in_data):
    # get and convert the data to float
    audio_data = np.fromstring(in_data, np.int16)
    # Fast Fourier Transform, 10*log10(abs) is to scale it to dB
    # and make sure it's not imaginary
    dfft = 10.*np.log10(abs(np.fft.rfft(audio_data)))

    # Force the new data into the plot, but without redrawing axes.
    # If uses plt.draw(), axes are re-drawn every time
    #print audio_data[0:10]
    #print dfft[0:10]
    #print
    li.set_xdata(np.arange(len(audio_data)))
    li.set_ydata(audio_data)
    li2.set_xdata(np.arange(len(dfft))*10.)
    li2.set_ydata(dfft)

    # Show the updated plot, but without blocking
    plt.pause(0.01)
    if keep_going:
        return True
    else:
        return False

p = pyaudio.PyAudio()
volume = 0.5     # range [0.0, 1.0]
chunk = 1024  # Record in chunks of 1024 samples
sample_format = pyaudio.paInt16  # 16 bits per sample
record_channels = 1
fs = 44100  # Record at 44100 samples per second
seconds = 3
filename = "output.wav"
f = 5000        # sine frequency, Hz, may be float
duration = 0.2

# generate samples, note conversion to float32 array
samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)

#for paFloat32 sample values must be in range [-1.0, 1.0]
streamPlay = p.open(format=pyaudio.paFloat32,
                channels=2,
                rate=fs,
                output=True)
streamRecord = p.open(format=sample_format,
                channels=record_channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames
#streamPlay.start_stream()
# play. May repeat with different volume values (if done interactively)
data_list = []
for i in range(0, int(fs / chunk * seconds)):
    streamPlay.write(volume * samples)
    data  = streamRecord.read(chunk)
    signal_gm = np.frombuffer(data, dtype="int16")
    data_list.extend(signal_gm)
    frames.append(data)
streamPlay.stop_stream()
streamPlay.close()
streamRecord.stop_stream()
streamRecord.close()
p.terminate()

print('Finished recording')
plt.plot(data_list)
plt.show()
# Save the recorded data as a WAV file
wf = wave.open(filename, 'wb')
wf.setnchannels(record_channels)
wf.setsampwidth(p.get_sample_size(sample_format))
wf.setframerate(fs)
wf.writeframes(b''.join(frames))
wf.close()