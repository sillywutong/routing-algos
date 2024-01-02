from algorithms import flooding
from networks import example_network

# construct network

g, routers, hosts = example_network.generate_japan_network(10)
source = input("Please input source ipv4 address: ")
target = input("Please input target ipv4 address: ")
print(f"Sending packet from {hosts[source].connected_router_id +1} to {hosts[target].connected_router_id+1}, path: ")
s = flooding.flooding(hosts[source].connected_router_id, hosts[target].connected_router_id, g, routers)
print(f"Total distance: {s}")

print(f"Forwarding tables of all routers: ")
for r in routers:
    print(r.node_id, r.forwarding_table)
