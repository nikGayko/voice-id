import io
import json
# def load_database(path: str) -> dict:
#     with open(path, mode='r') as file:
#         return json.load(file)
import os

from identification.models import Record


# def database_centroids(path: str) -> list:
#     points = []
#     centers = []
#
#     database = load_database(path)
#     for person, records in database.items():
#         last_point: NPoint
#         for _, mfcc in records.items():
#             mean = list_mean(mfcc)
#             last_point = NPoint(person, mean)
#             points.append(last_point)
#         centers.append(last_point)
#
#     centroids = k_mean(points, centers)
#     return centroids


def save_record(db_path: str, person_name: str, record: Record):
    __check_database__(db_path)
    with open(db_path, mode='r+') as file:
        database = json.load(file)
        file.seek(0)

        if "users" not in database:
            database.setdefault("users", {})

        users = database["users"]

        if person_name not in users:
            users.setdefault(person_name, {})

        person = users[person_name]

        if "records" not in person:
            person.setdefault("records", {})

        records = person["records"]

        if record.title in records:
            records[record.title] = record.json()
        else:
            records.setdefault(record.title, record.json())

        json.dump(database, file, sort_keys=True, indent=4, ensure_ascii=False)

        file.close()


def __check_database__(path: str):
    if os.path.isfile(path) and os.access(path, os.R_OK):
        print("File exists and is readable")
    else:
        print("Either file is missing or is not readable, creating file...")
        with io.open(path, 'w') as file:
            file.write(json.dumps({}))
