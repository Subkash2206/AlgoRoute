# Astar.py

import osmnx as ox
import heapq
import networkx as nx
import geopandas as gpd
from shapely.geometry import Polygon
from typing import List, Optional


def heuristic(graph: nx.MultiDiGraph, node1: int, node2: int) -> float:
    """
    Calculates the straight-line distance (heuristic) between two nodes.
    """
    point1 = (graph.nodes[node1]['y'], graph.nodes[node1]['x'])
    point2 = (graph.nodes[node2]['y'], graph.nodes[node2]['x'])
    return ox.distance.great_circle(*point1, *point2)


def my_a_star(graph: nx.MultiDiGraph, start_node: int, end_node: int) -> Optional[List[int]]:
    """
    Finds the fastest path based on travel time using the A* algorithm.
    """
    distances = {node: float('inf') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}
    distances[start_node] = 0
    priority_queue = [(0 + heuristic(graph, start_node, end_node), start_node)]

    while priority_queue:
        current_priority, current_node = heapq.heappop(priority_queue)

        if current_node == end_node:
            break

        if current_priority > distances[current_node] + heuristic(graph, current_node, end_node):
            continue

        for neighbor in graph.neighbors(current_node):
            edge_data = graph.get_edge_data(current_node, neighbor)
            travel_time = edge_data[0].get('travel_time', float('inf'))
            new_distance = distances[current_node] + travel_time

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                new_priority = new_distance + heuristic(graph, neighbor, end_node)
                heapq.heappush(priority_queue, (new_priority, neighbor))

    path = []
    current = end_node
    if predecessors[current] is not None or current == start_node:
        while current is not None:
            path.append(current)
            current = predecessors[current]
        path.reverse()
        return path
    else:
        return None


def apply_rush_hour_slowdown(graph: nx.MultiDiGraph, hour: int) -> nx.MultiDiGraph:
    """
    Applies a slowdown factor to main roads during rush hour.
    """
    new_graph = graph.copy()
    slowdown_factor = 3.0

    if 8 <= hour < 10 or 17 <= hour < 19:
        for u, v, data in new_graph.edges(data=True):
            if data.get('highway') in ['primary', 'secondary']:
                data['travel_time'] *= slowdown_factor

    return new_graph


def generate_isochrone(graph: nx.MultiDiGraph, start_node: int, trip_time_seconds: float) -> Optional[Polygon]:
    """
    Generates a polygon representing the area reachable from a start node
    within a given travel time.
    """
    try:
        subgraph = nx.ego_graph(graph, start_node, radius=trip_time_seconds, distance="travel_time")

        nodes_gdf = ox.graph_to_gdfs(subgraph, edges=False)
        if nodes_gdf.empty:
            return None

        # Create a polygon that covers all the reachable nodes
        return nodes_gdf.unary_union.convex_hull
    except Exception:
        return None