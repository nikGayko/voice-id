from core import mfcc
from identification import database_utils as db
from identification.MenuOptions import MenuOptions
from identification import cluster_utils as cluster
import ntpath

from identification.models import Record


class Manager:
    __DATABASE_PATH__: str

    def __init__(self, database_path: str):
        self.__DATABASE_PATH__ = database_path

    def start(self):
        option: MenuOptions = None
        while option is None or option is not MenuOptions.EXIT:

            self.__print_options__()
            option = self.__handle_option__()

            if option == MenuOptions.ADD_USER:
                self.__add_new_user__()
            elif option == MenuOptions.ADD_RECORD:
                pass
            elif option == MenuOptions.RECOGNIZE:
                pass

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

    def __add_new_user__(self):
        print("Input absolute path to audio file")
        file_path = str(input())

        print("Input user name")
        user_name = str(input())

        self.process_record(file_path, user_name)

    def process_record(self, file_path: str, user_name: str):
        coefficient = mfcc.process(file_path)
        centroid = cluster.list_mean(coefficient)
        file_name = ntpath.basename(file_path)

        record = Record(file_name, centroid, coefficient)
        db.save_record(self.__DATABASE_PATH__, user_name, record)

# def recognize_person(self, file_path: str):
#     centroids = database_centroids()
#     mfcc = processor.process(file_path)
#     mean_mfcc = list_mean(mfcc)
#
#     result = {}
#     for center in centroids:
#         distance = ManhattanDistance(center.points, mean_mfcc)
#         result.setdefault(center.title, distance)
#
#     print(result)

# def ManhattanDistance(lhr: list, rhs: list) -> float:
# result = 0.0
# for l_item, r_item in zip(lhr, rhs):
#     result += abs(l_item - r_item)
# return result
