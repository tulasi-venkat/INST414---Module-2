import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# loads in dataset
file_path = 'Final_Report_of_the_Asian_American_Quality_of_Life__AAQoL_.csv'
data = pd.read_csv(file_path)

# selects relevent columns
data = data[['Survey ID', 'Age', 'Ethnicity']].dropna()

# builds the graph with grouping
G = nx.Graph()

# adds nodes with attributes
for idx, row in data.iterrows():
    G.add_node(row['Survey ID'], age=row['Age'], ethnicity=row['Ethnicity'])

# groups by 'Age' and adds edges within each age group
for age, group in data.groupby('Age'):
    ids = group['Survey ID'].values
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            G.add_edge(ids[i], ids[j])

# groups by 'Ethnicity' and adds edges within each ethnicity group
for ethnicity, group in data.groupby('Ethnicity'):
    ids = group['Survey ID'].values
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            G.add_edge(ids[i], ids[j])

# calculates degree centrality
degree_centrality = nx.degree_centrality(G)

# adjusts node size and color based on centrality
node_sizes = [v * 2000 for v in degree_centrality.values()]
node_colors = [v for v in degree_centrality.values()]

# visualizse network
plt.figure(figsize=(12, 8))
pos = nx.spring_layout(G, seed=42)  # Seed for consistent layout
nx.draw_networkx_edges(G, pos, alpha=0.3)  # Lighter edges for less clutter

# draws nodes with sizes and colors based on centrality
nodes = nx.draw_networkx_nodes(
    G, pos, node_size=node_sizes, node_color=node_colors, cmap=plt.cm.Blues, edgecolors="black"
)

# labels the top 5 most central nodes
top_nodes = sorted(degree_centrality, key=degree_centrality.get, reverse=True)[:5]
labels = {node: node for node in top_nodes}
nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_color="darkblue")

# adds colorbar for node centrality using nodes as the mappable object
plt.colorbar(nodes, label='Degree Centrality')

plt.title("Network Visualization of Shared Demographic Attributes")
plt.show()
