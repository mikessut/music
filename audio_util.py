import pyaudio
import struct
import numpy as np


p = pyaudio.PyAudio()

# Open a .Stream object to write the WAV file to
# 'output = True' indicates that the sound will be played rather than recorded
stream = p.open(format = pyaudio.paFloat32,
                channels = 1,
                rate = 44100,
                # frames_per_buffer = 1024,
                output = True)


def pyaudioPlay(num, den, f0=440):
    fs = 44100
    tf = .75
    
    t = np.arange(0, tf, 1 / fs)
    y = np.sin(2 * np.pi * t * f0 * num / den)
    
    stream.write(struct.pack('f' * len(y), *y))


def pyaudioPlayF(f):
    fs = 44100
    tf = .75
    
    t = np.arange(0, tf, 1 / fs)
    y = np.sin(2 * np.pi * t * f)
    
    stream.write(struct.pack('f' * len(y), *y))


def play(num, den, f0=440):
    """
    works with jupyter lab
    """
    fs = 20000
    tf = 0.75
    t = np.arange(0, tf, 1 / fs)
    y = np.sin(2 * np.pi * t * f0 * num / den)
    display(Audio(y, rate=fs, autoplay=True))
    time.sleep(tf + .05)


# f = 2**(note_ratio / 12)
NOTE_RATIO = {
        'A': 0,
        'A#': 1,
        'Bb': 1,
        'B': 2,
        'C': 3,
        'C#': 4,
        'Db': 4,
        'D': 5,
        'D#': 6,
        'Eb': 6,
        'E': 7,
        'F': 8,
        'F#': 9,
        'Gb': 9,
        'G': 10,
        'G#': 11,
        'Ab': 11,
        'A': 0,
}

C4 = 261.626


# (num, den)
SCALE_RATIO = np.array([
    (1, 1),   # C
    (9, 8),   # D 
    (5, 4),   # E
    (4, 3),   # F
    (3, 2),   # G
    (5, 3),   # A
    (15, 8),  # B
    (2, 1),   # C
])


def note2f(note: str, f_A=440):
    return f_A * 2**(NOTE_RATIO[note] / 12)


def f2note(f, f_A=440):
    n = int(round(np.log(f / f_A) / np.log(2) * 12))
    if n > 11:
        return f2note(f / 2, f_A)
    elif n < 0:
        return f2note(f * 2, f_A)
    else:
        return next(k for k, v in NOTE_RATIO.items() if v == n)
    

class Interval:
        
    def __mul__(self, other):
        return self.n * other


class Third(Interval):
    n = 4


class MinThird(Interval):
    n = 3


class Fifth(Interval):
    n = 7


class Note:

    def __init__(self, val: type[float | str]):
        if isinstance(val, str):
            self._f = note2f(val)
        elif isinstance(val, float):
            self._f = val
        else:
            raise ValueError

    def interval(self, n: type[int | Interval]):
        if isinstance(n, Interval):
            n = n.n
        return Note(self._f * 2**(n / 12))

    def twelfth(self, f0=C4):
        return int(round(np.log(self._f / f0) / np.log(2) * 12))

    def __repr__(self):
        return f"<Note: {f2note(self._f)}>"

    def __add__(self, other):
        return self.interval(other)

    def __sub__(self, other):
        if isinstance(other, Note):
            i = Interval()
            i.n = int(round(np.log(self._f / other._f) / np.log(2) * 12))
            return i
        elif isinstance(other, Interval):
            return self.interval(-other.n)

    def freq(self, fmin, fmax):
        f = self._f
        while f > fmax:
            f /= 2
        while f < fmin:
            f *= 2
        return f

    def name(self):
        return f2note(self._f)