import sys
sys.path.append('..')
from objects import nodes
import networkx as nx
import numpy as np
import struct
import settings
import random

def generate_gaussian_network(n, nh):
    # randomly generate a gaussian partition network with 1. n routers; 2. only 1 connected components; 3. randomly connect nh hosts to some routers. 
    g = nx.gaussian_random_partition_graph(n, n/4, n/8, 0.6, 0.4, directed=False)
    while nx.is_strongly_connected(g) == False:
        print("not connected.")
        g = nx.gaussian_random_partition_graph(n, n/4, n/8, 0.6, 0.4, directed=False)
    nx.set_node_attributes(g, 0, "is_host")
    nx.set_node_attributes(g, {i:i for i in range(n)}, "id")
    e = g.number_of_edges()
    #g.add_nodes_from(list(range(n, n+nh)), is_host = 1)
    nx.set_edge_attributes(g, list([random.randint(settings.MIN_DIST, settings.MAX_DIST) for _ in range(n)]), "dist") # node distance
    routers = [nodes.Router(id=_) for _ in range(n)] # create routers
    hosts = []
    n_bits = 32-(int(nh) & 0xFFFFFFFF).bit_length()
    prefix = random.getrandbits(n_bits) # randomly generate ip address prefix
    for host in range(n, n+nh):
        v = random.choice(range(n))
        ipaddress = (prefix << 32-n_bits) + (host - n) # assign prefix + i as the ip address for each host
        g.add_node(host, is_host = 1, id=host)
        g.add_edge(v, host, dist=random.randint(settings.MIN_DIST, settings.MAX_DIST))
        #h = nodes.Host(id=host, ipaddress_bin=bytes(ipaddress))
        ip_bytes = ipaddress.to_bytes(4, 'big')
        ip_str = '.'.join([str(ip_bytes[i]) for i in range(4)])
        h = nodes.Host(id=host, ipaddress_bin=ip_bytes, ipaddress_str = ip_str)
        hosts.append(h)
    print(f"Graph with {n} nodes, {e} edges, {nh} hosts.")
    return g, routers, hosts

_, _, hosts = generate_gaussian_network(30, 10)
for h in hosts:
    print(h.ipaddress_str)

