#!/usr/bin/env python3

import sys
import math
import random

from common import write_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def two_opt(tour, dist): # 説明は同階層のdocument.mdを参照
    N = len(tour)
    improved = True
    n = 0
    while improved and n <= 300:
        n += 1
        improved = False
        for i in range(1, N):
            for j in range(i + 1, N + 1):
                if j - i == 1: continue  # 隣接ノード間だけでは経路の改善ができないのでスキップ
                # 4点に関して辺を組み替えた方が短ければ
                if dist[tour[i-1]][tour[i]] + dist[tour[j-1]][tour[j%N]] > dist[tour[i-1]][tour[j-1]] + dist[tour[i]][tour[j%N]]:
                    tour[i:j] = reversed(tour[i:j])
                    improved = True
                else:# j == Nの時にはif条件を満たした場合入れ替え
                    if random.random() < math.exp(-0.1*(dist[tour[i-1]][tour[j-1]] + dist[tour[i]][tour[j%N]]-dist[tour[i-1]][tour[i]] + dist[tour[j-1]][tour[j%N]])):
                        tour[i:j] = reversed(tour[i:j])
        print(n)
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

    tour = two_opt(tour, dist)
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    write_tour(tour, 'output_6.csv')
