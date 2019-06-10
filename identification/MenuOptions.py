from enum import Enum


class MenuOptions(Enum):
    ADD_RECORD = 1
    RECOGNIZE = 2
    EXIT = 0

    def description(self) -> str:
        if self == MenuOptions.ADD_RECORD:
            return "{}. Add record to database".format(self.value)
        elif self == MenuOptions.RECOGNIZE:
            return "{}. Recognize person".format(self.value)
        elif self == MenuOptions.EXIT:
            return "{}. Exit".format(self.value)

    @staticmethod
    def all_values() -> list:
        return [option.value for option in MenuOptions]
