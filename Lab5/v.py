"""Pass input directly to output.

https://app.assembla.com/spaces/portaudio/git/source/master/test/patest_wire.c

"""
import argparse
import queue
import sys
import scipy.signal
import sounddevice as sd
import numpy as np  # Make sure NumPy is loaded before it is used in the callback
from scipy.signal import butter, lfilter, freqz
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import time

def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    '-l', '--list-devices', action='store_true',
    help='show list of audio devices and exit')
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser])
parser.add_argument(
    '-t', '--interval', type=float, default=30,
    help='minimum time between plot updates (default: %(default)s ms)')
parser.add_argument(
    '-i', '--input-device', type=int_or_str,
    help='input device (numeric ID or substring)')
parser.add_argument(
    '-o', '--output-device', type=int_or_str,
    help='output device (numeric ID or substring)')
parser.add_argument(
    'channels', type=int, default=[1], nargs='*', metavar='CHANNEL',
    help='input channels to plot (default: the first)')
parser.add_argument('--dtype', help='audio data type')
parser.add_argument('--samplerate', type=float, help='sampling rate')
parser.add_argument('--blocksize', type=int, help='block size')
parser.add_argument('--latency', type=float, help='latency in seconds')
args = parser.parse_args(remaining)

if any(c < 1 for c in args.channels):
    parser.error('argument CHANNEL: must be >= 1')
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1

# Buffer for feeding samples to plot
q = queue.Queue()

# Indexing variable for generating the sine wave sound
start_idx = 0

fig, ax = plt.subplots()
fig.set_facecolor('black')
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
ax.set_facecolor("black")
xdata, ydata = [], []
ln, = plt.plot([], [], 'go')

order = 5

sampling_freq = 5000

cutoff_freq = 2

sampling_duration = 5

number_of_samples = sampling_freq * sampling_duration
normalized_cutoff_freq = 2 * cutoff_freq / sampling_freq
numerator_coeffs, denominator_coeffs = scipy.signal.butter(order, normalized_cutoff_freq)


def init():
    ax.set_xlim(0, 2*np.pi)
    ax.set_ylim(-0.1**-17, 0.1**-17)
    return ln,

def update(frame):

    while True:
        try:
            data = q.get_nowait()
            print(data)
            ln.set_data(2, data)
        except queue.Empty:
            break

    return ln,


try:
    length = int(200 * args.samplerate / (1000 * 10))
    plotdata = np.zeros((length, len(args.channels)))



    def callback(indata, outdata, frames, time, status):
        if status:
            print(status)
        global start_idx

        # Generate the sine wave for output
        t = (start_idx + np.arange(frames)) / args.samplerate
        t = t.reshape(-1, 1)
        #print(len(indata[::1, mapping]))
        outdata[:] = 0.5 * np.sin(2 * np.pi * 500 * t)
        start_idx += frames

        # Plot the received microphone input
        filtered_signal = scipy.signal.lfilter(numerator_coeffs, denominator_coeffs, outdata * indata[::1, mapping])

        q.put(filtered_signal)


    ani = FuncAnimation(fig, update, interval=args.interval,init_func=init, blit=True)

    with sd.Stream(device=(args.input_device, args.output_device),
                   samplerate=args.samplerate, blocksize=args.blocksize,
                   dtype=args.dtype, latency=args.latency,
                   channels=2, callback=callback):
        plt.show()

except KeyboardInterrupt:
    parser.exit('')
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))
