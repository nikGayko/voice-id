from enum import Enum


class MenuOptions(Enum):
    ADD_USER = 1
    ADD_RECORD = 2
    RECOGNIZE = 3
    EXIT = 0

    def description(self) -> str:
        if self == MenuOptions.ADD_USER:
            return "1. Add new user"
        elif self == MenuOptions.ADD_RECORD:
            return "2. Add new record to user"
        elif self == MenuOptions.RECOGNIZE:
            return "3. Recognize person"
        elif self == MenuOptions.EXIT:
            return "0. Exit"

    @staticmethod
    def all_values() -> list:
        return [option.value for option in MenuOptions]
