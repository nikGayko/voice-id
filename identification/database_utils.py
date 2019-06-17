import io
import json
import os

from mfcc.models import NPoint
from identification.models import Centroid, Record


def person_centroids(db_path: str, person: str) -> list:
    __check_database__(db_path)
    with open(db_path, mode='r+') as file:
        database = json.load(file)
        file.seek(0)

        centroids = []

        all_persons = database.get("users", {})
        person = all_persons.get(person, {})
        records = person.get("records", {})
        for _, record in records.items():
            centroid = record.get("centroid", [])
            centroids.append(NPoint(centroid))

        file.close()
        return centroids


def all_centroids(db_path: str) -> list:
    with open(db_path, mode='r+') as file:
        database = json.load(file)
        file.seek(0)

        centroids = []

        users = database.get("users", {})
        for user_name, value in users.items():
            centroid = value.get("centroid", [])
            centroids.append(Centroid(user_name, centroid))

        file.close()
        return centroids


def add_record(db_path: str, person_name: str, record: Record):
    __check_database__(db_path)
    with open(db_path, mode='r+') as file:
        database = json.load(file)
        file.seek(0)

        if "users" not in database:
            database.setdefault("users", {})

        users_json = database["users"]

        if person_name not in users_json:
            users_json.setdefault(person_name, {})

        person_json = users_json[person_name]

        if "records" not in person_json:
            person_json.setdefault("records", {})

        records_json = person_json["records"]

        if record.title in records_json:
            records_json[record.title] = record.json()
        else:
            records_json.setdefault(record.title, record.json())

        json.dump(database, file, sort_keys=True, indent=4, ensure_ascii=False)
        file.close()


def update_person_centroid(db_path: str, centroid: Centroid):
    __check_database__(db_path)
    with open(db_path, mode='r+') as file:
        database = json.load(file)
        file.seek(0)

        if "users" not in database:
            database.setdefault("users", {})

        users_json = database["users"]

        if centroid.title not in users_json:
            users_json.setdefault(centroid.title, {})

        person_json = users_json[centroid.title]

        if "centroid" in person_json:
            person_json["centroid"] = centroid.points
        else:
            person_json.setdefault("centroid", centroid.points)

        json.dump(database, file, sort_keys=True, indent=4, ensure_ascii=False)
        file.close()


def all_users(db_path: str) -> list:
    __check_database__(db_path)
    with open(db_path, mode='r+') as file:
        database = json.load(file)
        file.seek(0)

        users: dict = database.get("users", {})
        return list(users.keys())


def remove_user(db_path: str, person_name: str):
    __check_database__(db_path)
    with open(db_path, mode='w+') as file:
        database = json.load(file)
        file.seek(0)
        users: dict = database.get("users", {})

        if person_name in users:
            pass
            # users.pop(person_name, None)
            # json.dump(database, file, sort_keys=True, indent=4, ensure_ascii=False)

        file.close()


def remove_all(db_path: str):
    __check_database__(db_path)
    with open(db_path, mode='r+') as file:
        database = json.load(file)
        file.seek(0)

        if "users" in database:
            pass
            # del database["users"]
            # json.dump(database, file, sort_keys=True, indent=4, ensure_ascii=False)

        file.close()


def __check_database__(path: str):
    if os.path.isfile(path) and os.access(path, os.R_OK):
        pass
    else:
        print("Either file is missing or is not readable, creating file...")
        with io.open(path, 'w') as file:
            file.write(json.dumps({}))
            file.close()
