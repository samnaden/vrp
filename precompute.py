from dataclasses import dataclass

from util import get_euclidean_distance


@dataclass
class Load:
    id: int
    start: tuple[float, float]
    end: tuple[float, float]
    route_distance: float
    start_dist_from_depot: float
    end_dist_from_depot: float
    nearest_loads: list[tuple[int, float]] = None


def get_loads(input_filepath: str) -> dict[int, Load]:
    loads = {}

    with open(input_filepath) as f:
        for line in f:
            if "loadNumber" in line:
                continue

            row = line.split()

            load_id = int(row[0]) - 1

            begin = row[1]
            begin = begin.replace("(", "").replace(")", "").split(",")
            begin = tuple([float(coord) for coord in begin])

            end = row[2]
            end = end.replace("(", "").replace(")", "").split(",")
            end = tuple([float(coord) for coord in end])

            route_distance = get_euclidean_distance(begin, end)
            start_distance_from_depot = get_euclidean_distance((0.0, 0.0), (begin))
            end_distance_from_depot = get_euclidean_distance((0.0, 0.0), end)

            load = Load(
                id=load_id,
                start=begin,
                end=end,
                route_distance=route_distance,
                start_dist_from_depot=start_distance_from_depot,
                end_dist_from_depot=end_distance_from_depot
            )

            loads[load_id] = load

    return loads


def update_loads_with_nearest_neighbors(loads: dict[int, Load]):
    """mutates loads by populating the field nearest_loads"""

    n = len(loads)
    distance_matrix = [[0.0]*n for _ in range(n)]

    for i in range(0, n):
        for j in range(0, n):
            if i != j:
                load_a = loads[i]
                load_b = loads[j]
                distance = get_euclidean_distance(load_a.end, load_b.start)
                distance_matrix[i][j] = distance

    for load_id in range(0, n):
        distances = distance_matrix[load_id]
        load_id_by_distance = {}
        for neighbor_load_id in range(0, n):
            if neighbor_load_id != load_id:
                distance = distances[neighbor_load_id]
                load_id_by_distance[distance] = neighbor_load_id

        load_id_by_distance_sorted = dict(sorted(load_id_by_distance.items()))
        nearest_loads = []
        for distance, neighbor_load_id in load_id_by_distance_sorted.items():
            nearest_loads.append((neighbor_load_id, distance))
        loads[load_id].nearest_loads = nearest_loads
