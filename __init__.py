"""
MIT License

Copyright (c) 2019  Nikita Gayko

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import wave
import numpy
from enum import Enum

types = {
    1: numpy.int8,
    2: numpy.int16,
    4: numpy.int32
}


class TestRecords(Enum):
    BASE_TEST_1 = '../test-records/Дипломная работа, тестовая речь.wav'
    SCREAM = '../test-records/Крик.wav'
    WHISPER = '../test-records/Шепот.wav'
    NOISE = '../test-records/Шум.wav'


def main():
    wav_file = wave.open(TestRecords.SCREAM.value)
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav_file.getparams()
    frames = wav_file.readframes(nframes)
    amplitudes = numpy.fromstring(frames, dtype=types[sampwidth])
    print(amplitudes)


def average_amplitude(file_name):
    audio_file = wave.open(file_name)
    frame = audio_file.readframes(1)

    average_result = {}
    amplitudes = []
    frame_number = 0

    while frame != b'':
        amplitude = convert_bytes(frame, is_big_indian=False)
        amplitude = amplitude / pow(2, 15)
        # put amplitude in range -1 to 1
        normalized = amplitude - 1
        amplitudes.append(normalized)

        frame_number += 1

        if frame_number > audio_file.getframerate():
            key = int(frame_number / audio_file.getframerate())
            value = numpy.mean(amplitudes)
            average_result.setdefault(key, value)

            amplitudes = []
            frame_number = 0

        frame = audio_file.readframes(1)

    audio_file.close()
    return average_result


def grouped_by_time(file_name):
    audio_file = wave.open(file_name)
    frame = audio_file.readframes(1)
    ranges = {}
    frame_count = 0

    while frame != b'':
        frame_count += 1

        amplitude = convert_bytes(frame, audio_file.getsampwidth(), is_big_indian=False)
        range = -pow(2, 15)
        while range + 500 < amplitude:
            range += 500

        key = '{}_{}'.format(int(frame_count / 10000), range)
        curr_value = ranges.get(key, 0)
        ranges.setdefault(key, 0)
        ranges[key] = curr_value + 1

        frame = audio_file.readframes(1)

    audio_file.close()
    return ranges


def convert_bytes(audio_frame, sample_widht, is_big_indian=True):
    samples = numpy.fromstring(audio_frame, dtype=types[sample_widht])
    return samples[0]
    # ordered_bytes = list(reversed(byte_array)) if is_big_indian else byte_array
    #
    # result = 0
    #
    # for z in range(len(ordered_bytes)):
    #     byte = ordered_bytes[z]
    #     result += pow(255, z) * byte
    #
    # return result


def write_dict(dict, file_name):
    csv = 'Amplitude, Sample count\n'
    for k in sorted(dict):
        csv += "{},{}\n".format(k, dict[k])
    write_file(csv, file_name)


def write_file(file_data, name):
    file = open(name, 'w')
    file.write(file_data)
    file.close()


if __name__ == "__main__":
    main()
