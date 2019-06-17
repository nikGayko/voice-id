class NPoint:
    points: list

    def __init__(self, points: list):
        self.points = points

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'points {}'.format(self.points)

    def __eq__(self, other):
        return self.points == other.points
