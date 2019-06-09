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
import json
import wave
from enum import Enum

import numpy

import mfcc as processor
import voice_recognition
from NPoint import NPoint

types = {
    1: numpy.int8,
    2: numpy.int16,
    4: numpy.int32
}


class TestRecordsHN(Enum):
    BASE_TEST_1 = 'Гайко Никита -Дипломная работа, тестовая речь.wav'
    SCREAM = 'Гайко Никита - Крик.wav'
    WHISPER = 'Гайко Никита - Шепот.wav'

    WEATHER = 'Гайко Никита - Прекрасная погода на улице.wav'
    RAIN = 'Гайко Никита - Дождь, мы все промокнем.wav'
    GRADUATE_WORK = 'Гайко Никита -Дипломная работа, тестовая речь.wav'

    PAUSES = 'Гайко Никита - большие паузы.wav'

    LOUD = 'Гайко Никита - Громко.wav'
    QUIET = 'Гайко Никита - Тихо.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class TestRecordsHE(Enum):
    HUSH = 'Гайко Елена - Люди спят, давай потише.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class TestRecordsHU(Enum):
    SCHOOL = 'Гайко Юля - в школе мне надоело.wav'
    WEATHER = 'Гайко Юля - какой хороший день.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class TestRecordsAM(Enum):
    CLOTHES = 'Артур Манцевич - женская одежда.wav'
    KULICHI = 'Артур Манцевич - Куличи.wav'
    GOD_ADV = 'Артур Манцевич - реклама бога.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class TestRecordsAH(Enum):
    FOOTBALL = 'Алексей Ханько - Футбол.wav'
    WEATHER = 'Алексей Ханько - Погода.wav'
    COURSE_WORK = 'Алексей Ханько - дипломная записка.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class TestRecordsOther(Enum):
    NOBODY = 'Никого - Шум.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class Users(Enum):
    NIKITA_HAIKO = 'Nikita Haiko'
    ULA_HAIKO = 'Ula Haiko'
    ELENA_HAIKO = 'Yelena Haiko'
    ALEXEI_HANKO = 'Alexey Hanko'
    ARTUR_MANCEVICH = 'Artur Mancevich'


def main():
    wav_file = wave.open(TestRecords.SCREAM.value)
    (nchannels, sampwidth, framerate, nframes, comptype, compname) = wav_file.getparams()
    frames = wav_file.readframes(nframes)
    amplitudes = numpy.fromstring(frames, dtype=types[sampwidth])
    max_amplitude = abs(max(amplitudes, key=abs))
    normalized_amplitudes = list(map(lambda ampl: ampl / max_amplitude, amplitudes))
    voice_recognition.apply_window(normalized_amplitudes, sample_rate=framerate)


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


# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


def main_1():
    add_new_record(TestRecordsHN.LOUD, Users.NIKITA_HAIKO)
    # add_new_record(TestRecordsHN.QUIET, Users.NIKITA_HAIKO)
    # add_new_record(TestRecordsHN.QUIET1, Users.NIKITA_HAIKO)
    # recognize_person(TestRecordsHN.RAIN.rel_path())

# nikita_scream = mfcc.process(TestRecordsHN.SCREAM.value)
# nikita_weather = mfcc.process(TestRecordsHN.WEATHER.value)
#
# coef = min(len(nikita_weather), len(nikita_scream))
#
# nikita_graduate = normalized_mean(nikita_scream, coef / len(nikita_scream))
# nikita_weather = normalized_mean(nikita_weather, coef / len(nikita_weather))
#
# distance = ManhattanDistance(nikita_graduate, nikita_weather)
# print("distance: {}".format(distance))

# for weather_index in range(len(nikita_weather)):
#     for grad_index in range(len(nikita_graduate)):
#         distance = ManhattanDistance(nikita_graduate[grad_index], nikita_weather[weather_index])
#         print("[{};{}] distance: {}".format(weather_index, grad_index, distance))

# nikita_graduate = list_mean(mfcc.process(TestRecordsHN.GRADUATE_WORK.value))
# nikita_weather = list_mean(mfcc.process(TestRecordsHN.WEATHER.value))
# nikita_scream = list_mean(mfcc.process(TestRecordsHN.SCREAM.value))
# nikita_pauses = list_mean(mfcc.process(TestRecordsHN.PAUSES.value))
#
# yelena_hush = list_mean(mfcc.process(TestRecordsHE.HUSH.value))
#
# ula_weather = list_mean(mfcc.process(TestRecordsHU.WEATHER.value))
# ula_school = list_mean(mfcc.process(TestRecordsHU.SCHOOL.value))
#
# points = [nikita_graduate, nikita_weather, nikita_scream, nikita_pauses, yelena_hush, ula_weather, ula_school]
# centers = [nikita_graduate, yelena_hush, ula_school]
#
# cluster_centers = k_mean(points, centers=centers)
#
# nobody = list_mean(mfcc.process(TestRecordsOther.NOBODY.value))


# points = [nikita_graduate, nikita_weather, nikita_scream, nikita_pauses, yelena_hush, ula_weather, ula_school]
# centers = [nikita_graduate, yelena_hush, ula_school]
#
# cluster_centers = k_mean(points, centers=centers)
#
# nobody = list_mean(mfcc.process(TestRecordsOther.NOBODY.value))

# print('nikita_graduate to nikita_weather {}'.format(ManhattanDistance(nikita_graduate, nikita_weather)))
# print('nikita_weather to nikita_scream {}'.format(ManhattanDistance(nikita_weather, nikita_scream)))
# print('nikita_graduate to nikita_scream {}'.format(ManhattanDistance(nikita_graduate, nikita_scream)))
#
# print('nikita_weather to nikita_pauses {}'.format(ManhattanDistance(nikita_weather, nikita_pauses)))
# print('nikita_graduate to nikita_pauses {}'.format(ManhattanDistance(nikita_graduate, nikita_pauses)))
#
# print('yelena_hush to ula_weather {}'.format(ManhattanDistance(yelena_hush, ula_weather)))
# print('yelena_hush to ula_school {}'.format(ManhattanDistance(yelena_hush, ula_school)))
# print('yelena_hush to nikita_weather {}'.format(ManhattanDistance(yelena_hush, ula_school)))
# print('yelena_hush to nikita_scream {}'.format(ManhattanDistance(yelena_hush, ula_school)))
# print('yelena_hush to nikita_pauses {}'.format(ManhattanDistance(yelena_hush, nikita_pauses)))
#
# print('ula_school to ula_weather {}'.format(ManhattanDistance(ula_school, ula_weather)))
# print('ula_weather to nikita_weather {}'.format(ManhattanDistance(ula_weather, nikita_weather)))
# print('ula_weather to nikita_graduate {}'.format(ManhattanDistance(ula_weather, nikita_graduate)))
# print('ula_weather to nikita_pauses {}'.format(ManhattanDistance(ula_weather, nikita_pauses)))
#
# print('nobody to nikita_graduate {}'.format(ManhattanDistance(nobody, nikita_graduate)))
# print('nobody to ula_school {}'.format(ManhattanDistance(nobody, ula_school)))
# print('nobody to yelena_hush {}'.format(ManhattanDistance(nobody, yelena_hush)))
# print('nobody to nikita_pauses {}'.format(ManhattanDistance(nobody, nikita_pauses)))


def add_new_record(file_path: Enum, person: Enum):
    mfcc = processor.process(file_path.rel_path())
    save_mfcc(person.value, file_path.value, mfcc)


def recognize_person(file_path: str):
    centroids = database_centroids()
    mfcc = processor.process(file_path)
    mean_mfcc = list_mean(mfcc)

    result = {}
    for center in centroids:
        distance = ManhattanDistance(center.points, mean_mfcc)
        result.setdefault(center.title, distance)

    print(result)


def database_centroids() -> list:
    points = []
    centers = []

    database = load_database()
    for person, records in database.items():
        last_point: NPoint
        for _, mfcc in records.items():
            mean = list_mean(mfcc)
            last_point = NPoint(person, mean)
            points.append(last_point)
        centers.append(last_point)

    centroids = k_mean(points, centers)
    return centroids


def list_mean(array: list) -> list:
    result = [0] * len(array[0])
    for sub_list in array:
        for index in range(len(sub_list)):
            result[index] += sub_list[index]

    result = [result[index] / len(array) for index in range(len(result))]

    return result


def k_mean(points: list, centers: list, count: int = 10) -> list:
    if count < 0:
        return centers

    clusters = []
    for _ in centers:
        clusters.append([])

    for point in points:
        distances = [ManhattanDistance(point.points, center.points) for center in centers]
        index = distances.index(min(distances))
        clusters[index].append(point)

    new_centers = []
    for cluster in clusters:
        cluster_points = list(map(lambda p: p.points, cluster))
        mean = list_mean(cluster_points)

        title = centers[clusters.index(cluster)].title
        new_centers.append(NPoint(title, mean))

    print('-' * 30)
    for cluster, center in zip(clusters, centers):
        print('CLUSTER')
        print('Center {}'.format(center))
        for point in cluster:
            print(point)
    print('-' * 30)

    if new_centers == centers:
        return new_centers
    else:
        return k_mean(points, new_centers, count - 1)


def ManhattanDistance(lhr: list, rhs: list) -> float:
    result = 0.0
    for l_item, r_item in zip(lhr, rhs):
        result += abs(l_item - r_item)
    return result


DATABASE_PATH = 'mfcc_database.json'


def load_database() -> dict:
    with open(DATABASE_PATH, mode='r') as file:
        return json.load(file)


def save_mfcc(person_node: str, audio_node: str, data: list):
    with open(DATABASE_PATH, mode='r+') as file:
        database = json.load(file)
        file.seek(0)

        if person_node in database:
            database[person_node].setdefault(audio_node, data)
        else:
            database.setdefault(person_node, {audio_node: data})
        json.dump(database, file, sort_keys=True, indent=4, ensure_ascii=False)

        file.close()


if __name__ == "__main__":
    main_1()
