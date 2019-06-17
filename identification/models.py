from mfcc.models import NPoint


class Record:
    title: str
    centroid: NPoint
    values: list

    def __init__(self, title: str, centroid: NPoint, values: list):
        super().__init__()
        self.title = title
        self.centroid = centroid
        self.values = values

    def json(self):
        return {"centroid": self.centroid.points, "values": self.values}


class Person:
    name: str
    centroid: NPoint
    records: [Record]

    def __init__(self, name: str, centroid: NPoint, records: [Record]):
        self.name = name
        self.centroid = centroid
        self.records = records


class Centroid(NPoint):
    title: str

    def __init__(self, title: str, points: list):
        self.title = title
        self.points = points


class Distance:
    title_from: str = None
    title_to: str = None
    distance: float

    def __init__(self, distance: float):
        self.distance = distance

    def __init__(self, distance: float, title_to: str):
        self.distance = distance
        self.title_to = title_to

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'title to {0}; distance: {1}'.format(self.title_to, self.distance)