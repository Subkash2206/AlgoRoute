
# AlgoRoute: A Dynamic Routing and Road Network Analysis Engine

AlgoRoute is a Python-based application designed to solve complex pathfinding problems on real-world road networks. The system implements and compares multiple graph traversal algorithms, simulates dynamic traffic conditions, and performs advanced geospatial analysis to model emergency vehicle response times. The entire engine is wrapped in an interactive web interface built with Streamlit.

This project serves as a comprehensive demonstration of skills in algorithm design, data structures, geospatial data processing, and application development.

---

## Key Features

- **Dynamic Map Ingestion:** The application can dynamically fetch and model any city's road network from OpenStreetMap data using the OSMnx library.
- **Classic and Heuristic Pathfinding:**
  - **Dijkstra's Algorithm:** Implemented from scratch to find the mathematically shortest path based on physical distance.
  - **A\* Algorithm:** Implemented from scratch to find the fastest path, using travel time as the edge weight and the Haversine distance as an admissible heuristic.
- **Dynamic Traffic Simulation:** A simulation model that dynamically adjusts edge weights (travel times) on primary and secondary roads to mimic rush hour conditions, demonstrating the A\* algorithm's ability to find alternative, faster routes.
- **Isochrone Generation (Response Zone Analysis):** The application can generate isochrone polygons, visualizing all reachable points from a given origin within a specified travel time. This is a critical tool for emergency services resource planning and performance analysis.
- **Interactive User Interface:** A clean, functional user interface built with Streamlit that allows for the selection of map areas, start/end points, algorithms, and simulation parameters.

---

## Technical Methodology

- **Graph Representation:** Road networks are modeled as directed graphs (`networkx.MultiDiGraph`), where intersections are nodes and road segments are edges. Graph data is acquired and parsed using **OSMnx**.
- **Cost Functions:** The system utilizes two primary cost functions for pathfinding:
  1.  **Distance (`length`):** Used by Dijkstra's algorithm to find the geometrically shortest path.
  2.  **Time (`travel_time`):** Calculated based on edge length and imputed speed limits. This is used by the A\* algorithm to find the fastest path, which is dynamically altered by the traffic simulation.
- **Isochrone Calculation:** Response zones are calculated by generating a subgraph containing all nodes reachable within a given travel time limit using `networkx.ego_graph`. A convex hull is then computed from the coordinates of these nodes using **Shapely** and **GeoPandas** to create the final isochrone polygon.

---

## Technology Stack

- **Core Language:** Python 3
- **Geospatial Analysis:**
  - OSMnx
  - NetworkX
  - GeoPandas
  - Shapely
- **Web Interface:**
  - Streamlit
  - Folium (for map rendering)
- **Core Libraries:** heapq (for priority queue implementation)

---

## Setup and Execution

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/Subkash2206/AlgoRoute.git](https://github.com/Subkash2206/AlgoRoute.git)
    cd AlgoRoute
    ```

2.  **Create and Activate a Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    All required libraries are listed in the `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit Application:**
    ```bash
    streamlit run app.py
    ```
The application will then be accessible in your web browser.
