import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Load the dataset
data = pd.read_csv('/Users/sanya/Downloads/DataChallenge2024_forStudents (1)/data/MainTask/SPNDataChallenge_columns.csv')

# Map SESSION to expertise levels
data['EXPERTISE'] = data['SESSION'].map({1: 'Consultant', 2: 'Registrar', 3: 'Novice'})

# Normalize TASK_MINUS_BASELINE for better variability
data['TASK_MINUS_BASELINE_NORMALIZED'] = (
    data['TASK_MINUS_BASELINE'] - data['TASK_MINUS_BASELINE'].mean()
) / data['TASK_MINUS_BASELINE'].std()

# Function to perform weighted network analysis and calculate general graph metrics
def weighted_network_analysis(data):
    graph_metrics = {}

    for expertise in ['Consultant', 'Registrar', 'Novice']:
        subset = data[data['EXPERTISE'] == expertise]

        if subset.empty:
            continue

        # Use all channels as rows and metrics as columns
        session_data = subset.pivot_table(
            index='CHANNEL', 
            values=['TASK_MINUS_BASELINE_NORMALIZED', 'AREA_UNDER_CURVE_TASK', 'STD_TASK'], 
            aggfunc='mean'
        ).dropna()

        if session_data.empty:
            continue

        # Compute pairwise correlations across metrics
        corr_matrix = session_data.T.corr()

        # Create a weighted graph using NetworkX
        G = nx.Graph()
        for i, row in corr_matrix.iterrows():
            for j, value in row.items():
                if i != j and not np.isnan(value) and abs(value) > 0.4:  # Add edges based on correlation threshold
                    G.add_edge(i, j, weight=abs(value))  # Use absolute value to avoid negative weights

        if len(G.nodes) < 4 or G.number_of_edges() == 0:
            continue

        # Calculate weighted graph metrics
        weighted_degree_centrality = nx.degree_centrality(G)
        weighted_clustering_coefficient = nx.clustering(G, weight='weight')
        graph_density = nx.density(G)
        weighted_shortest_path_length = nx.average_shortest_path_length(G, weight='weight') if nx.is_connected(G) else None

        # Calculate general graph metrics
        node_degrees = dict(G.degree())
        avg_clustering_coefficient = nx.average_clustering(G, weight='weight')
        network_diameter = nx.diameter(G) if nx.is_connected(G) else None
        small_world_index = nx.sigma(G) if nx.is_connected(G) else None
        betweenness_centrality = nx.betweenness_centrality(G, weight='weight')

        # Store metrics
        graph_metrics[expertise] = {
            "Weighted Degree Centrality": weighted_degree_centrality,
            "Weighted Clustering Coefficient": weighted_clustering_coefficient,
            "Graph Density": graph_density,
            "Weighted Shortest Path Length": weighted_shortest_path_length,
            "Node Degrees": node_degrees,
            "Average Clustering Coefficient": avg_clustering_coefficient,
            "Network Diameter": network_diameter,
            "Small World Index": small_world_index,
            "Betweenness Centrality": betweenness_centrality
        }

        # Visualize the weighted graph
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(G)
        nx.draw(
            G, pos, with_labels=True, node_color='lightblue', edge_color='gray', 
            node_size=500, font_size=10, width=[d['weight'] for (u, v, d) in G.edges(data=True)]
        )
        plt.title(f"Weighted Graph for {expertise}")
        plt.show()

    return graph_metrics

# Run the updated weighted network analysis
weighted_graph_metrics = weighted_network_analysis(data)

# Convert the results to a DataFrame for better visualization
weighted_metrics_df = pd.DataFrame(weighted_graph_metrics).T

# Save the results to a CSV file
weighted_metrics_df.to_csv('Weighted_Network_Analysis_Metrics.csv')

# Display the results
print("Weighted Network Analysis Metrics:")
print(weighted_metrics_df)

# Provide a download link for the CSV file
import IPython.display as display
display.display(display.HTML("<a href='Weighted_Network_Analysis_Metrics.csv' download>Download Weighted Network Analysis Metrics</a>"))
