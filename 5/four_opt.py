#!/usr/bin/env python3

import sys
import math

from common import write_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def four_opt(tour, dist):
    N = len(tour)
    improved = True

    while improved:
        improved = False
        for i in range(N - 3):
            for j in range(i + 2, N - 1):
                for k in range(j + 2, N - 1):
                    for l in range(k + 2, N + (i > 0)):  # N + (i > 0) to wrap around to the start
                        # Get current edges
                        a, b = tour[i], tour[(i + 1) % N]
                        c, d = tour[j], tour[(j + 1) % N]
                        e, f = tour[k], tour[(k + 1) % N]
                        g, h = tour[l % N], tour[(l + 1) % N]

                        # Calculate old and new distances
                        d_old = dist[a][b] + dist[c][d] + dist[e][f] + dist[g][h]
                        d_new = dist[a][c] + dist[b][d] + dist[e][g] + dist[f][h]
                        
                        if d_new < d_old:
                            # Perform 4-opt move
                            new_tour = tour[:i+1] + list(reversed(tour[i+1:j+1])) + list(reversed(tour[j+1:k+1])) + list(reversed(tour[k+1:l+1])) + tour[l+1:]
                            tour[:] = new_tour[:]
                            improved = True
    return tour

def solve(cities):
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])

    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city

    tour = four_opt(tour, dist)
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    write_tour(tour, 'output_6.csv')
