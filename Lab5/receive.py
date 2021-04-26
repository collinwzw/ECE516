import pyaudio
import numpy as np
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt



fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_facecolor("black")
xdata, ydata = [], []
ln, = plt.plot([], [], 'go')

def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-5, 20)
    return ln,

def update(data):
    ln.set_data(2, data)
    return ln,

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

streamRecord = p.open(format=sample_format,
                channels=record_channels,
                rate=fs,
                frames_per_buffer=chunk,
                input=True)

frames = []  # Initialize array to store frames
#streamPlay.start_stream()
# play. May repeat with different volume values (if done interactively)
data_list = []
while 1:
    data  = streamRecord.read(chunk)
    signal_gm = np.frombuffer(data, dtype="int16")
    data_list.extend(signal_gm)
    frames.append(data)

    ani = FuncAnimation(fig, update, frames=i,
                    init_func=init, blit=True)
plt.show()
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