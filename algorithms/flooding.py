import networkx as nx
from collections import deque
from collections import defaultdict
def flooding(source, target, graph, routers):
    # BFS with calculating the shortest path
    visited = dict() # when the node is first visited
    parent = dict() # the last node on the shortest path
    parent[source] = None
    queue = deque([(source, source, 0)])
    path_length = 0x7FFFFFFF
    while queue:
        parent_node, current_node, l = queue.popleft()
        if graph.nodes[current_node]['is_host'] == 1:
            continue
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
                if v != parent_node and graph.nodes[v]['is_host'] == 0:
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
    children = construct_path_tree(source, parent, visited)
    update_fwd_dfs(source, children, routers)
    return path_length

def construct_path_tree(src, parents, visits):
    children = defaultdict(list)
    for v in visits:
        if v == src:
            continue
        children[parents[v]].append(v)
    return children
def update_fwd_dfs(node, children, routers):
    hosts_list = routers[node].connected_hosts
    for h in hosts_list:
        routers[node].forwarding_table[h] = node
    if node not in children:
        # leaf
        return hosts_list
    # not a leaf, dfs children
    for u in children[node]:
        h_list = update_fwd_dfs(u, children, routers)
        for h in h_list:
            routers[node].forwarding_table[h] = u
        hosts_list.extend(h_list)
    return hosts_list

'''
def update_fwd_path(parents, src, target, routers):
    current_node = target
    hosts_target = routers[target].connected_hosts
    for h in hosts_target:
        routers[target].forwarding_table[h] = target
    while current_node != src:
        for h in hosts_target:
            routers[parents[current_node]].forwarding_table[h] = current_node
        current_node = parents[current_node]
def update_fwd(parents, visits, src, target, routers):
    # on the path from src to target:
    update_fwd_path(parents=parents, src=src, target=target, routers=routers)
    for v in visits:
        update_fwd_path(parents, src, v, routers)
'''