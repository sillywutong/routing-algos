import networkx as nx
from collections import deque

def flooding(source, target, graph):
    # BFS with calculating the shortest path
    visited = dict() # when the node is first visited
    parent = dict() # the last node on the shortest path
    parent[source] = None
    queue = deque([(source, source, 0)])
    path_length = 0x7FFFFFFF
    while queue:
        parent_node, current_node, l = queue.popleft()
        if current_node == target:
            if l < path_length: # found a shorter path
                path_length = l
                parent[target] = parent_node
                visited[target] = l
            continue
        if current_node not in visited or l < visited[current_node]: # not visited before
            visited[current_node] = l
            parent[current_node] = parent_node
            neighbors = nx.neighbors(graph, current_node)
            for v in neighbors:
                if v != parent_node:
                    #parent[v] = current_node
                    queue.append((current_node, v, l + graph[current_node][v]['dist']))
    # trace back
    route = []
    current_node = target
    while current_node != source:
        route.insert(0, current_node)
        current_node = parent[current_node]
    route.insert(0, source)
    print('->'.join([str(u+1) for u in route]))
    return path_length
