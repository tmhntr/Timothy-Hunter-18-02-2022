class mynetwork():
    def __init__(self):
        self._adj = {}
        self.attributes = {}

    def add_node(self, new_node, **attr) -> None:
        if (not new_node.__hash__()):
            raise ValueError(f"{new_node} is not a hashable object.")
        else:
            self._adj[new_node] = {}
            self.attributes[new_node] = {}
            # print(attr)
            for k, v in attr.items():
                self.attributes[new_node][k] = v

    def add_nodes_from(self, nodes_for_adding, **attr):
        if isinstance(nodes_for_adding[0], tuple):
            for node, node_attr in nodes_for_adding:
                node_attr.update(attr)
                self.add_node(node, **node_attr)
        else:
            for node in nodes_for_adding:
                self.add_node(node, **attr)

    def remove_node(self, n) -> None:
        # Remove node from all node adjacencies
        # TODO: for directed graph this will have to search through all nodes
        for k in self._adj[n]:
            self._adj[k].pop(n)
        # remove node from attributes
        self.attributes.pop(n)
        # remove node from adjacencies
        self._adj.pop(n)

    def __getitem__(self, n):
        return self._adj[n]

    def __contains__(self, n):
        return n in self._adj

    def add_edge(self, u_node, v_node, **attr) -> None:
        if u_node not in self._adj:
            self.add_node(u_node)
        if v_node not in self._adj:
            self.add_node(v_node)
        # add en edge in the explicitly declared direction
        if v_node in self._adj[u_node]:
            self._adj[u_node][v_node].update(attr)
        else:
            self._adj[u_node][v_node] = attr
        # add en edge in the implicit direction
        if u_node in self._adj[v_node]:
            self._adj[v_node][u_node].update(attr)
        else:
            self._adj[v_node][u_node] = attr

    def remove_edge(self, u_node, v_node) -> None:
        self._adj[u_node].pop(v_node)
        # for undirected graph this line is commented out
        self._adj[v_node].pop(u_node)

    def update(self, edges=None, nodes=None):
        if hasattr(edges, 'nodes') and hasattr(edges, 'edges'):
            for k, v in edges.nodes.items():
                self.add_node(k, **v)
            for e in edges.edges:
                self.add_edge(*e)
        elif edges:
            for e in edges:
                self.add_edge(*e)
        if nodes:
            for n in nodes:
                self.add_node(n)

    def clear(self) -> None:
        del self._adj
        del self.attributes
        self._adj = {}
        self.attributes = {}

    def __iter__(self):
        return iter(self._adj)

    def has_node(self, n):
        return n in self._adj

    def has_edge(self, u, v):
        return (u in self._adj[v] and v in self._adj[u])

    def get_edge_data(self, u, v, default=None):
        pass

    def neighbors(self, n):
        pass

    def adjacency(self):
        pass

    def nbunch_iter(self, nbunch=None):
        pass

    def order(self):
        pass

    def number_of_nodes(self):
        pass

    def __len__(self):
        pass

    def size(self):
        pass

    def number_of_edges(self, u=None, v=None) -> int:
        pass

    def __getattribute__(self, __name: str):
        if __name == 'nodes':
            return self.attributes
        return object.__getattribute__(self, __name)
