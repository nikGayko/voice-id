import wave
from math import cos
from math import pi

import numpy
import pyqtgraph as pg

from mfcc.errors import ChannelNumberError, BitsDepthError, FramrateError

types = {
    1: numpy.int8,
    2: numpy.int16,
    4: numpy.int32
}

SECTION_SEC = 0.128

MFCC_SIZE = 12
MIN_FREQUENCY = 300
MAX_FREQUENCY = 8000


def process(file_name: str) -> list:
    wav_file = wave.open(file_name)
    __validate__(wav_file)

    (nchannels, bits_depth, framerate, frames_count, _, _) = wav_file.getparams()

    frames = wav_file.readframes(frames_count)
    amplitudes = numpy.fromstring(frames, dtype=types[bits_depth])

    max_amplitude = abs(max(amplitudes, key=abs))
    normalized_amplitudes = list(map(lambda ampl: ampl / max_amplitude, amplitudes))

    section_length = int(framerate * SECTION_SEC)
    sections_count = int(frames_count / section_length)

    sections = __devide_audio__(normalized_amplitudes, section_length, sections_count)

    factors = [transform(samples, MFCC_SIZE, framerate, MAX_FREQUENCY, MIN_FREQUENCY) for samples in sections]
    return factors


def __validate__(wav_file):
    (nchannels, bits_depth, framerate, frames_count, _, _) = wav_file.getparams()

    if nchannels != 1:
        print("WAV should have mono channels")
        raise ChannelNumberError

    if bits_depth < 2:
        print("WAV should have 2 bytes per frame")
        raise BitsDepthError

    if framerate < 41500:
        print("WAV framerate should be more than 41500Hz")
        raise FramrateError


def __devide_audio__(amplitudes: list, length: int, count: int) -> list:
    sections = []
    for index in range(count):
        start_pointer = int(length / 2 * index)
        end_pointer = start_pointer + length
        section = amplitudes[start_pointer:end_pointer]
        sections.append(section)

    return sections


def transform(samples: list, mfcc_size: int, framerate: int, max_frequency, min_frequency) -> list:
    length = len(samples)
    dft_samples = dft(samples)

    filters = mel_filters(mfcc_size, length, framerate, max_frequency, min_frequency)

    power = calc_power(dft_samples, length, filters, mfcc_size)
    result = dct_transform(power, mfcc_size)
    return result


def dft(samples: list) -> list:
    dft_samples = numpy.fft.fft(samples)
    absolute_samples = [numpy.absolute(sample) for sample in dft_samples]
    samples_len = len(samples)
    windowed_samples = [absolute_samples[index] * hamming_window(index, samples_len) for index in
                        range(samples_len)]

    return windowed_samples


def hamming_window(n: float, N: int) -> float:
    return 0.53836 - 0.46164 * cos(2 * pi * n / (N - 1))


# [401.25, 622.50, 843.75, 1065.00, 1286.25, 1507.50, 1728.74, 1949.99, 2171.24, 2392.49, 2613.74, 2834.99]
# h[i] = [300, 517.33, 781.90, 1103.97, 1496.04, 1973.32, 2554.33, 3261.62, 4122.63, 5170.76, 6446.70, 8000]
def mel_filters(mfcc_size: int, frame_size: int, frequency: int, freq_max: int, freq_min: int) -> list:
    mel_min = convert_to_mel(freq_min)
    mel_max = convert_to_mel(freq_max)
    mel_filter_step = (mel_max - mel_min) / (mfcc_size + 1)

    mel_bin = [mel_min + mel_filter_step * index for index in range(mfcc_size + 2)]
    frequency_bin = [convert_from_mel(mel) for mel in mel_bin]
    key_sample_index = [int((frame_size + 1) * freq / frequency) for freq in frequency_bin]

    filter_bank = []
    for index in range(mfcc_size):
        filter_bank.append([0] * frame_size)

    for m in range(1, mfcc_size + 1):
        for k in range(frame_size):
            if key_sample_index[m - 1] <= k <= key_sample_index[m]:
                filter_bank[m - 1][k] = (k - key_sample_index[m - 1]) / (key_sample_index[m] - key_sample_index[m - 1])
            elif key_sample_index[m] < k <= key_sample_index[m + 1]:
                filter_bank[m - 1][k] = (key_sample_index[m + 1] - k) / (key_sample_index[m + 1] - key_sample_index[m])
            else:
                filter_bank[m - 1][k] = 0

    return filter_bank


def calc_power(dft_section: list, frame_length: int, mel_filter: list, mfcc_size: int) -> list:
    log_power = [0] * mfcc_size
    for m in range(mfcc_size):
        for k in range(frame_length):
            log_power[m] += mel_filter[m][k] * pow(dft_section[k], 2)
        log_power[m] = numpy.log(log_power[m])
    return log_power


def dct_transform(data: list, length: int) -> list:
    result = [0] * length
    for n in range(length):
        for m in range(length):
            result[n] += data[m] * cos(pi * n * (m + 0.5) / length)

    return result


def convert_to_mel(freq: int) -> float:
    return 1127 * numpy.log(1 + freq / 700)
    # return 2595 * numpy.log10(1 + freq / 700)


def convert_from_mel(mel: float) -> float:
    return 700 * (pow(numpy.e, mel / 1127) - 1)


def show_array(array, title=None):
    plot = pg.plot(array)
    plot.plotItem.showGrid(x=True, y=True, alpha=0.5)
    plot.plotItem.setTitle(title)


def default_pen():
    return pg.mkPen('b', width=0.5)


def config_pg():
    pg.setConfigOption('background', 'w')
    pg.setConfigOption('foreground', 'k')
