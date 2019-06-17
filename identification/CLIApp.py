from identification import core
from identification import database_utils as db
from identification.MenuOptions import MenuOptions


class CLIApp:
    __DATABASE_PATH__: str

    def __init__(self, database_path: str):
        self.__DATABASE_PATH__ = database_path

    def start(self):
        option: MenuOptions = None
        while option is None or option is not MenuOptions.EXIT:

            self.__print_options__()
            option = self.__handle_option__()

            if option == MenuOptions.ADD_RECORD:
                self.__add_new_record__()
            elif option == MenuOptions.RECOGNIZE:
                self.__recognize_person__()
            elif option == MenuOptions.REMOVE_USER:
                self.__remove_person__()
            elif option == MenuOptions.REMOVE_ALL:
                self.__remove_all__()

    def __print_options__(self):
        print("Choose one of available options:")
        [print(option.description()) for option in MenuOptions]

    def __handle_option__(self) -> MenuOptions:
        try:
            option = int(input())
            return MenuOptions(option)
        except ValueError:
            values = MenuOptions.all_values()
            print("ERROR!!!")
            print("Input must be integer number from {0} to {1}".format(min(values), max(values)))
            return None

        # Option 1 - add new user

    def __add_new_record__(self):
        file_path = self.__request_path__()

        print("Input new user name or select one of suggested:")
        all_names = db.all_users(self.__DATABASE_PATH__)
        [print("{}. {}".format(index, all_names[index])) for index in range(len(all_names))]

        chosen_opt = input()
        try:
            index = int(chosen_opt)
            person_name = all_names[index]
        except ValueError:
            person_name = chosen_opt

        print("processing {} record...".format(person_name))
        record = core.process_record(file_path)
        db.add_record(self.__DATABASE_PATH__, person_name, record)

        core.update_centroid(self.__DATABASE_PATH__, person_name)
        print("database updated")

        # Option 2 - recognize person

    def __recognize_person__(self):
        file_path = self.__request_path__()

        print("processing...")
        distances = core.recognize(self.__DATABASE_PATH__, file_path)
        print("Result:")
        distances.sort(key=lambda dist: dist.distance)
        [print("{} distance - {}".format(dist.title_to, dist.distance)) for dist in distances]

    def __request_path__(self) -> str:
        print("Input absolute path to audio file")
        return str(input())

    # Option 3 - recognize person

    def __remove_person__(self):
        print("Select person:")

        print("Input select one user name:")
        all_names = db.all_users(self.__DATABASE_PATH__)
        [print("{}. {}".format(index, all_names[index])) for index in range(len(all_names))]

        try:
            index = int(input())
            person_name = all_names[index]
            db.remove_user(self.__DATABASE_PATH__, person_name)
            print("{} removed".format(person_name))
        except (ValueError, IndexError):
            print("ERROR!!!\nInvalid option")

    # Option 4 - recognize person

    def __remove_all__(self):
        db.remove_all(self.__DATABASE_PATH__)
        print("All users removed")
