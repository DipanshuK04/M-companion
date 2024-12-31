import pandas as pd
import networkx as nx

# Load the CSV file
data = pd.read_csv('Mumbai Local Train Dataset.csv', encoding='latin1')
# print(data['Station'].tolist())
# Create a MultiGraph (or switch to nx.Graph if multiple edges aren't needed)
G = nx.MultiGraph()

# Add edges with the 'line' attribute
for i in range(154 - 1):  # Use len(data) for flexibility
    if data['Line'][i] == data['Line'][i + 1]:  # Check if the line matches
        G.add_edge(
            data['Station'][i],
            data['Station'][i + 1],
            key=f"{data['Line'][i]}_{i}",  # Unique key for each edge
            line=data['Line'][i]  # Line information is added as an attribute
        )

# Define the shortest path function
def find_shortest_path(graph, start, end):
    # Get the shortest path (unweighted)
    path = nx.shortest_path(graph, source=start, target=end)
    detailed_path = []
    short_path = []
    short_path.append(start)
    prev_line = None

    for i in range(len(path) - 1):
        station = path[i]
        next_station = path[i + 1]
        
        # Access edge attributes (line) from MultiGraph
        edge_data = graph.get_edge_data(station, next_station)
        if edge_data:
            # Extract the line attribute (fetch from the first edge, assuming one exists)
            line = list(edge_data.values())[0]['line']
            if line != prev_line:
                if prev_line:  # Only add this if it's not the first station
                    detailed_path.append(f"Change to {line} line at {station} station")
                    short_path.append(f"--{prev_line} line-->")
                    short_path.append(station)
            prev_line = line
        
        detailed_path.append(station)
    detailed_path.append(end)
    if len(short_path) < 2:
        detailed_path.append(line)
    short_path.append(f"--{line} line-->")
    short_path.append(end)
    return detailed_path, short_path

# Example usage
detailed, short = find_shortest_path(G, 'Kalyan', 'CSMT')

print("Detailed Path:", detailed)
print("Short Path:", short)
