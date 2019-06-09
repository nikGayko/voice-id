class NPoint:
    title: str
    points: list

    def __init__(self, title: str, points: list):
        self.title = title
        self.points = points

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return 'Title {}; points {}'.format(self.title, self.points)

    def __eq__(self, other):
        return self.title == other.title and self.points == other.points
