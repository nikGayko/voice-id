from core.NPoint import NPoint


class Record:
    title: str
    centroid: NPoint
    values: list

    def __init__(self, title: str, centroid: list, values: list):
        super().__init__()
        self.title = title
        self.centroid = NPoint(centroid)
        self.values = values

    def json(self):
        return {"centroid": self.centroid.points, "values": self.values}


class Users:
    name: str
    centroid: NPoint
    records: [Record]
