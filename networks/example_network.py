import sys
sys.path.append('..')
from objects import nodes
import networkx as nx
import numpy as np
import struct
import settings
import random

def generate_japan_network(nh):
    # construct the JAPAN network. with nh hosts.
    g = nx.Graph()
    g.add_nodes_from(range(14), is_host=0, id={i: i for i in range(14)})
    g.add_edge(0, 1, dist = 160)
    g.add_edge(0, 2, dist = 240)
    g.add_edge(1, 3, dist = 240)
    g.add_edge(2, 4, dist = 240)
    g.add_edge(3, 4, dist = 80)
    g.add_edge(4, 5, dist = 40)
    g.add_edge(3, 5, dist = 40)
    g.add_edge(4, 6, dist = 80)
    g.add_edge(5, 7, dist = 160)
    g.add_edge(6, 7, dist = 80)
    g.add_edge(4, 8, dist = 240)
    g.add_edge(6, 11, dist = 240)
    g.add_edge(7, 9, dist = 160)
    g.add_edge(9, 11, dist = 40)
    g.add_edge(8, 11, dist = 240)
    g.add_edge(8, 13, dist = 240)
    g.add_edge(13, 11, dist = 240)
    g.add_edge(9, 10, dist = 40)
    g.add_edge(10, 11, dist = 40)
    g.add_edge(11, 12, dist = 320)
    g.add_edge(13, 12, dist = 160)
    g.add_edge(12, 10, dist = 320)
    routers = [nodes.Router(id=_) for _ in range(14)]
    hosts = []
    n_bits = 32-(int(nh) & 0xFFFFFFFF).bit_length()
    prefix = random.getrandbits(n_bits) # randomly generate ip address prefix
    ip_start = (prefix << 32-n_bits)
    ip_start_str = '.'.join([str(ip_start.to_bytes(4, 'big')[i]) for i in range(4)])
    for host in range(14, 14+nh):
        v = random.choice(range(14))
        ipaddress = ip_start + (host - 14) # assign prefix + i as the ip address for each host
        g.add_node(host, is_host = 1, id=host)
        g.add_edge(v, host, dist=random.randint(settings.MIN_DIST, settings.MAX_DIST))
        #h = nodes.Host(id=host, ipaddress_bin=bytes(ipaddress))
        ip_bytes = ipaddress.to_bytes(4, 'big')
        ip_str = '.'.join([str(ip_bytes[i]) for i in range(4)])
        h = nodes.Host(id=host, ipaddress_bin=ip_bytes, ipaddress_str = ip_str)
        hosts.append(h)
    print(f"Graph with {14} nodes, {22} edges, {nh} hosts.")
    print(f"ip address from {ip_start_str} to {ip_str}")
    return g, routers, hosts


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
    ip_start = (prefix << 32-n_bits)
    ip_start_str = '.'.join([str(ip_start.to_bytes(4, 'big')[i]) for i in range(4)])
    for host in range(n, n+nh):
        v = random.choice(range(n))
        ipaddress = ip_start + (host - n) # assign prefix + i as the ip address for each host
        g.add_node(host, is_host = 1, id=host)
        g.add_edge(v, host, dist=random.randint(settings.MIN_DIST, settings.MAX_DIST))
        #h = nodes.Host(id=host, ipaddress_bin=bytes(ipaddress))
        ip_bytes = ipaddress.to_bytes(4, 'big')
        ip_str = '.'.join([str(ip_bytes[i]) for i in range(4)])
        h = nodes.Host(id=host, ipaddress_bin=ip_bytes, ipaddress_str = ip_str)
        hosts.append(h)
    print(f"Graph with {n} nodes, {e} edges, {nh} hosts.")
    print(f"ip address from {ip_start_str} to {ip_str}")
    return g, routers, hosts

_, _, hosts = generate_japan_network(257)
for h in hosts:
    print(h.ipaddress_str)

