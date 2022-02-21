class mynetwork():
    def __init__(self) -> None:
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

        if v_node in self._adj[u_node]:
            self._adj[u_node][v_node].update(attr)
        else:
            self._adj[u_node][v_node] = attr

        # for undirected graph this line is commented out
        if u_node in self._adj[v_node]:
            self._adj[v_node][u_node].update(attr)
        else:
            self._adj[v_node][u_node] = attr

    def remove_edge(self, u_node, v_node) -> None:
        self._adj[u_node].pop(v_node)

        # for undirected graph this line is commented out
        self._adj[v_node].pop(u_node)

    def update(self, edges=None, nodes=None):
        pass

    def clear(self) -> None:
        pass

    def __iter__(self):
        pass

    def has_node(self, n):
        pass

    def has_edge(self, u, v):
        pass

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
