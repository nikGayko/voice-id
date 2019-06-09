from math import cos
from math import pi

import numpy as np
import pyqtgraph as pg

__TIME_SECTION_SEC__ = 0.128
__WINDOW_OVERLAP__ = 0.5


def apply_window(samples: list, sample_rate: int):
    samples_in_section = int(sample_rate * __TIME_SECTION_SEC__)

    sections_to_test = int(len(samples) / samples_in_section)
    # device to sections
    sections = []
    for z in range(0, sections_to_test):
        start_pointer = z * int(samples_in_section * __WINDOW_OVERLAP__)
        end_pointer = start_pointer + samples_in_section
        sections.append(samples[start_pointer:end_pointer])

    # disk_util.write_array_of_arrays(sections, file_name="Scream norm. ampl. sections 256ms (128ms per section).csv")

    windowed_sections = []
    hamming_weights = [__hamming_window__(index, samples_in_section) for index in range(samples_in_section)]

    for section in sections:
        windowed_samples = [weight * sample for weight, sample in zip(hamming_weights, section)]
        windowed_sections.append(windowed_samples)

    # disk_util.write_array_of_arrays(windowed_sections, file_name="Scream norm. ampl.
    # sections 256ms (128ms per section) + Hamming window.csv")

    dft_complex_sections = [np.fft.fft(win_section) for win_section in windowed_sections]
    dft_absolute_sections = []
    for complex_section in dft_complex_sections:
        abs_sections = [np.absolute(cmpl) for cmpl in complex_section]
        dft_absolute_sections.append(abs_sections)

    # mels_sections = []
    # for powed_dft in powed_dft_sections:
    #     mels_sec = [__to_mel__(sample) for sample in powed_dft]
    #     mels_sections.append(mels_sec)

    # absolute_dft_sections = []
    # for section in dft_sections:
    #     abs_section = [abs(sample) for sample in section]
    #     absolute_dft_sections.append(abs_section)

    # dft_real_sections = []
    # dft_imag_sections = []
    # for section in dft_sections:
    #     imag = [cmpl.imag for cmpl in section]
    #     real = [cmpl.real for cmpl in section]
    #     dft_real_sections.append(real)
    #     dft_imag_sections.append(imag)



    for index in range(0, len(sections)):
        start_pointer = int(samples_in_section / 2 * index)
        x_line = range(start_pointer, start_pointer + samples_in_section)

        pg.plot(x_line, dft_absolute_sections[index], pen='r')

        # pw = pg.plot(x_line, absolute_dft_sections[index], pen='r')
        # pw.plotItem.plot(x_line, windowed_sections[index], pen='b')

        # pw = pg.plot(x_line, sections[index], pen='r')
        # pw.plotItem.plot(x_line, windowed_sections[index], pen='g')
        # pw.plotItem.plot(x_line, hamming_weights, pen='b')

        # pw = pg.plot(x_line, dft_real_sections[index], pen='r')
        # pw.plotItem.plot(x_line, dft_imag_sections[index], pen='b')

    return samples


def __hamming_window__(n: float, N: int) -> float:
    return 0.53836 - 0.46164 * cos(2 * pi * n / (N - 1))


def __to_mel__(sample: float) -> float:
    return 2595 * np.log10(1 + sample / 700)