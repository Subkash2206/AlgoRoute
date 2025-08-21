# app.py

import streamlit as st
import osmnx as ox
import geopandas as gpd
# Corrected import statement
from routing_engine import my_dijkstra, my_a_star, apply_rush_hour_slowdown, generate_isochrone

# --- App Configuration ---
st.set_page_config(page_title="Routing Engine", layout="wide")


# --- Caching ---
@st.cache_resource
def load_graph_data(place_name):
    """
    Downloads, prepares, and caches the graph data for the specified location.
    """
    try:
        st.info(f"Loading map data for {place_name}... This may take a moment on first run.")
        G = ox.graph_from_place(place_name, network_type='drive')
        hwy_speeds = {"primary": 60, "secondary": 50, "tertiary": 40, "residential": 30, "unclassified": 25, "road": 25}
        G = ox.add_edge_speeds(G, hwy_speeds=hwy_speeds, fallback=30)
        G = ox.add_edge_travel_times(G)
        st.success(f"Map data for {place_name} loaded successfully!")
        return G
    except Exception as e:
        st.error(f"Could not load map data for '{place_name}'. Please check the name or try another. Error: {e}")
        return None


# --- Main App ---
st.title("Dynamic Emergency Routing Engine 🚑")

# --- User Inputs in Sidebar ---
with st.sidebar:
    st.header("Map Options")
    place_name_input = st.text_input("Enter a City or Place Name", "Rourkela, Odisha, India")

    st.header("Routing Options")
    app_mode = st.radio("Choose App Mode:", ("Find Route", "Analyze Response Zone"))

    if app_mode == "Find Route":
        origin_address = st.text_input("Start Location", "NIT Rourkela")
        destination_address = st.text_input("End Location", "Rourkela Railway Station")
        algorithm_choice = st.selectbox("Choose Algorithm:",
                                        ("A* (Fastest, with traffic)", "Dijkstra (Shortest Distance)"))

        hour_of_day = 14
        if "A*" in algorithm_choice:
            hour_of_day = st.slider("Select Hour of Day (for traffic)", 0, 23, 17)

        run_button = st.button("Find Route", type="primary")

    else:  # Analyze Response Zone
        start_point_address = st.text_input("Select Start Point", "Apollo Hospital, Rourkela")
        response_time = st.slider("Response Time (minutes)", 1, 15, 5)
        run_button = st.button("Analyze Zone", type="primary")

# Load the graph based on user input
G = load_graph_data(place_name_input)

# --- Map Display Area ---
st.header("Route Visualization")

if G:
    if run_button:
        with st.spinner("Calculating..."):
            try:
                if app_mode == "Find Route":
                    origin_point = ox.geocode(origin_address)
                    destination_point = ox.geocode(destination_address)
                    origin_node = ox.nearest_nodes(G, origin_point[1], origin_point[0])
                    destination_node = ox.nearest_nodes(G, destination_point[1], destination_point[0])

                    route = None
                    if "A*" in algorithm_choice:
                        G_traffic = apply_rush_hour_slowdown(G.copy(), hour=hour_of_day)
                        route = my_a_star(G_traffic, origin_node, destination_node)
                    else:
                        route = my_dijkstra(G, origin_node, destination_node)

                    if route:
                        st.success("Route found!")
                        # Use matplotlib for a static plot, which is compatible with all versions
                        fig, ax = ox.plot_graph_route(G, route, route_color='red', route_linewidth=4, node_size=0)
                        st.pyplot(fig)
                    else:
                        st.error("Could not find a route.")

                else:  # Analyze Response Zone
                    start_point = ox.geocode(start_point_address)
                    start_node = ox.nearest_nodes(G, start_point[1], start_point[0])
                    trip_time_seconds = response_time * 60

                    isochrone_polygon = generate_isochrone(G, start_node, trip_time_seconds)

                    if isochrone_polygon:
                        st.success(f"Response zone for {response_time} minutes calculated!")
                        fig, ax = ox.plot_graph(G, node_size=0, show=False, close=False)
                        # Plot the polygon on the matplotlib figure
                        patch = gpd.GeoSeries([isochrone_polygon]).plot(ax=ax, fc='blue', alpha=0.4)
                        st.pyplot(fig)
                    else:
                        st.error("Could not generate the response zone.")
            except Exception as e:
                st.error(f"An error occurred: {e}. Please ensure locations are within '{place_name_input}'.")
    else:
        st.info("Select options in the sidebar and click a button to begin.")
        # Generate a static plot for the base map
        fig, ax = ox.plot_graph(G, node_size=0, show=False, close=False)
        st.pyplot(fig)
else:
    st.warning("Map could not be loaded. Please enter a valid place name.")