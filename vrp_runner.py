import logging
import argparse
from typing import Optional

from precompute import Load, get_loads, update_loads_with_nearest_neighbors

MAX_DISTANCE = 12 * 60

logging.basicConfig(level="INFO", format="%(asctime)s %(levelname)-8.8s %(module)-25.25s:%(lineno)-5.5s %(message)s",)


def get_next_candidate(load: Load, seen_loads: set[int], all_loads: dict[int, Load]) -> tuple[Optional[Load], Optional[float]]:
    next_candidate = None
    next_dist = None
    for neighbor_id, dist in load.nearest_loads:
        if neighbor_id not in seen_loads:
            return all_loads[neighbor_id], dist

    return next_candidate, next_dist


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("input")

    args = parser.parse_args()

    input_ = args.input

    logging.info(f"parsing {input_}")
    loads = get_loads(input_)

    loads_closest_to_depot_by_start = list(loads.values())
    loads_closest_to_depot_by_start.sort(key=lambda x: x.start_dist_from_depot)

    logging.info("calculating nearest neighbors")
    update_loads_with_nearest_neighbors(loads)

    # the whole point of the code up until now is to collect all the information we need to do a greedy approach
    # see README for details
    all_routes = []
    all_distances = []
    accounted_for_loads = set()
    for load in loads_closest_to_depot_by_start:
        curr_route = []
        if load.id not in accounted_for_loads:
            curr_route.append(load.id)
            accounted_for_loads.add(load.id)
            distance_traveled = load.start_dist_from_depot + load.route_distance

            curr_load = load
            while True:
                next_candidate, next_dist = get_next_candidate(curr_load, accounted_for_loads, loads)
                if next_candidate is None:
                    break

                additional_distance = next_dist + next_candidate.route_distance + next_candidate.end_dist_from_depot
                if distance_traveled + additional_distance <= MAX_DISTANCE:
                    curr_route.append(next_candidate.id)
                    accounted_for_loads.add(next_candidate.id)
                    distance_traveled = distance_traveled + next_dist + next_candidate.route_distance
                    curr_load = next_candidate
                else:
                    break

            distance_traveled += curr_load.end_dist_from_depot
            all_distances.append(distance_traveled)
            all_routes.append(curr_route)
            logging.info(f"settled on route {curr_route} with distance {distance_traveled}")

    # remember to add 1 back to the route ids
    all_routes = [[z + 1 for z in y] for y in all_routes]

    num_drivers = 0
    total_driven_minutes = 0
    for i in range(0, len(all_routes)):
        route = all_routes[i]
        distance = all_distances[i]
        logging.info(route)
        logging.info(distance)
        logging.info("")

        num_drivers += 1
        total_driven_minutes += distance

    num_loads = len(loads)
    total_cost = (500 * num_drivers) + total_driven_minutes
    logging.info(f"num_loads={num_loads}, num_drivers={num_drivers}, total_driven_minutes={total_driven_minutes}, total_cost={total_cost}")
