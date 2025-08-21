# routing_engine.py

# Import the specific functions from your other scripts.
# This file acts as the central point of access for your routing algorithms.
from dijkstra import my_dijkstra
from Astar import my_a_star, apply_rush_hour_slowdown, heuristic, generate_isochrone

# The app.py file will now only need to import from this single engine file.