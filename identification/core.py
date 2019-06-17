import ntpath

from mfcc import mfcc
from identification import database_utils as db
from identification import math as cluster
from identification.models import Record, Centroid, Distance


def process_record(file_path: str) -> Record:
    coefficient = mfcc.process(file_path)
    centroid = cluster.list_mean(coefficient)
    file_name = ntpath.basename(file_path)
    record = Record(file_name, centroid, coefficient)
    return record


def update_centroid(db_path: str, person_name: str):
    centroid = recount_centroid(db_path, person_name)
    db.update_person_centroid(db_path, centroid)


def recount_centroid(db_path: str, person_name: str) -> Centroid:
    centroids = db.person_centroids(db_path, person_name)
    mean_centroid = cluster.list_mean(centroids)
    centroid = Centroid(person_name, mean_centroid.points)
    return centroid


def recognize(db_path, file_path: str) -> list:
    coefficients = mfcc.process(file_path)
    centroid = cluster.list_mean(coefficients)

    all_centroids = db.all_centroids(db_path)
    distances = []
    for person_centroid in all_centroids:
        dist = cluster.manhattan_distance(centroid.points, person_centroid.points)
        distances.append(Distance(dist, person_centroid.title))

    return distances
