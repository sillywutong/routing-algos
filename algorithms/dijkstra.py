def update_forwarding_table(routers, path, target):
    for router in routers:
        router.forwarding_table[target] = None  # 清空目标节点的转发表项

    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]
        if current_node not in routers:
            continue
        if next_node in routers:
            routers[current_node].forwarding_table[target] = next_node

def dijkstra(source, target, graph, routers):
    distances = {node: float('inf') for node in graph.nodes()}
    predecessors = {node: None for node in graph.nodes()}
    distances[source] = 0

    unvisited = set(graph.nodes())

    while unvisited:
        current_node = min(unvisited, key=lambda node: distances[node])

        if current_node == target:
            break

        unvisited.remove(current_node)

        for neighbor in graph.neighbors(current_node):
            if neighbor in unvisited:
                new_distance = distances[current_node] + graph[current_node][neighbor]['dist']
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node

    path = []
    current_node = target
    while current_node is not None:
        path.insert(0, current_node+1)
        current_node = predecessors[current_node]

    update_forwarding_table(routers, path, target)

    return distances[target], path
