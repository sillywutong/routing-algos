class Node:
    def __init__(self):
        pass
class Router(Node):
    def __init__(self, id):
        super(Router, self).__init__()
        self.forwarding_table = dict() # TODO: implement forwarding table update
        self.node_id = id
class Host(Node):
    def __init__(self, id, rid, ipaddress_bin, ipaddress_str):
        super(Host, self).__init__()
        self.ipaddress_bin = ipaddress_bin
        self.ipaddress_str = ipaddress_str
        self.node_id = id
        self.connected_router_id = rid