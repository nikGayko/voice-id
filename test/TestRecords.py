from enum import Enum


class HaikoNikita(Enum):
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


class HaikoElena(Enum):
    HUSH = 'Гайко Елена - Люди спят, давай потише.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class HaikoUla(Enum):
    SCHOOL = 'Гайко Юля - в школе мне надоело.wav'
    WEATHER = 'Гайко Юля - какой хороший день.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class ArturMancevich(Enum):
    CLOTHES = 'Артур Манцевич - женская одежда.wav'
    KULICHI = 'Артур Манцевич - Куличи.wav'
    GOD_ADV = 'Артур Манцевич - реклама бога.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class AlexeiHanko(Enum):
    FOOTBALL = 'Алексей Ханько - Футбол.wav'
    WEATHER = 'Алексей Ханько - Погода.wav'
    COURSE_WORK = 'Алексей Ханько - дипломная записка.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class Other(Enum):
    NOBODY = 'Никого - Шум.wav'

    def rel_path(self) -> str:
        return '../test-records/' + self.value


class Users(Enum):
    NIKITA_HAIKO = 'Nikita Haiko'
    ULA_HAIKO = 'Ula Haiko'
    ELENA_HAIKO = 'Yelena Haiko'
    ALEXEI_HANKO = 'Alexey Hanko'
    ARTUR_MANCEVICH = 'Artur Mancevich'
