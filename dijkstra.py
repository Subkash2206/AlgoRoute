# dijkstra.py

import heapq

def my_dijkstra(graph, start_node, end_node):
    """
    Finds the shortest path based on distance using Dijkstra's algorithm.
    """
    distances = {node: float('inf') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}
    distances[start_node] = 0
    priority_queue = [(0, start_node)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_distance > distances[current_node]:
            continue

        if current_node == end_node:
            break

        for neighbor in graph.neighbors(current_node):
            edge_data = graph.get_edge_data(current_node, neighbor)
            # Dijkstra uses 'length' for shortest distance
            length = edge_data[0].get('length', float('inf'))
            new_distance = distances[current_node] + length

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (new_distance, neighbor))

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