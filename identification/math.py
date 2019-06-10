from core.models import NPoint


def list_mean(array: list) -> NPoint:
    if all(isinstance(item, NPoint) for item in array):
        return list_mean([n_point.points for n_point in array])

    result = [0] * len(array[0])
    for sub_list in array:
        for index in range(len(sub_list)):
            result[index] += sub_list[index]

    result = [result[index] / len(array) for index in range(len(result))]

    return NPoint(result)


def k_mean(points: list, centers: list, count: int = 10) -> list:
    if count < 0:
        return centers

    clusters = []
    for _ in centers:
        clusters.append([])

    for point in points:
        distances = [ManhattanDistance(point.points, center.points) for center in centers]
        index = distances.index(min(distances))
        clusters[index].append(point)

    new_centers = []
    for cluster in clusters:
        cluster_points = list(map(lambda p: p.points, cluster))
        mean = list_mean(cluster_points)

        title = centers[clusters.index(cluster)].title
        new_centers.append(NPoint(title, mean))

    print('-' * 30)
    for cluster, center in zip(clusters, centers):
        print('CLUSTER')
        print('Center {}'.format(center))
        for point in cluster:
            print(point)
    print('-' * 30)

    if new_centers == centers:
        return new_centers
    else:
        return k_mean(points, new_centers, count - 1)


def manhattan_distance(lhr: list, rhs: list) -> float:
    result = 0.0
    for l_item, r_item in zip(lhr, rhs):
        result += abs(l_item - r_item)
    return result
