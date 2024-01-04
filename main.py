from algorithms import flooding
from algorithms import dijkstra
from networks import example_network
from algorithms import Bellman_ford
# construct network

g, routers, hosts = example_network.generate_japan_network(10)
source = input("Please input source ipv4 address: ")
target = input("Please input target ipv4 address: ")
print(f"Sending packet from {hosts[source].connected_router_id +1} to {hosts[target].connected_router_id+1}: ")
s = flooding.flooding(hosts[source].connected_router_id, hosts[target].connected_router_id, g, routers)
print(f"Flooding's total distance and path: {s}")
d = dijkstra.dijkstra(hosts[source].connected_router_id, hosts[target].connected_router_id, g, routers)
print(f"Dijkstra's total distance and path: {d}")
b = Bellman_ford.bellman_ford(hosts[source].connected_router_id, hosts[target].connected_router_id, g)
print(f"Bellman-Ford's total distance and path: {b}")
print()

