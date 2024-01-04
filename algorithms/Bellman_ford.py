import networkx as nx
def bellman_ford(source, target, graph):
    graph = graph.subgraph([n for n in graph.nodes() if graph.nodes[n]['is_host']==0])
    print(graph.edges(data=True))
    # Initialize distances and predecessors
    distances = {node: float('inf') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}
    distances[source] = 0

    # Relax edges repeatedly
    for _ in range(len(graph.nodes()) - 1):
        for u, v, data in graph.edges(data=True):
            if distances[u] + data['dist'] < distances[v]:
                distances[v] = distances[u] + data['dist']
                predecessors[v] = u
            elif distances[v] + data['dist'] < distances[u]:
                distances[u] = distances[v] + data['dist']
                predecessors[u] = v
                #print(distances)

    # Reconstruct the path
    print(distances, predecessors)
    path = []
    current_node = target
    while current_node is not None:
        path.insert(0, current_node+1)
        current_node = predecessors[current_node]

    return distances[target], path