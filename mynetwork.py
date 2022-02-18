from collections import OrderedDict


class mynetwork():
    def __init__(self) -> None:
        self.adj = {}
        self.attributes = {}

    def add_node(self, new_node, **attr) -> None:
        if (not new_node.__hash__()):
            raise ValueError(f"{new_node} is not a hashable object.")
        else:
            self.adj[new_node] = {}
            self.attributes[new_node] = {}
            # print(attr)
            for k, v in attr.items():
                self.attributes[new_node][k] = v

    def remove_node(self, n) -> None:
        # Remove node from all node adjacencies
        # TODO: for directed graph this will have to search through all nodes
        for k in self.adj[n]:
            self.adj[k].pop(n)

        # remove node from attributes
        self.attributes.pop(n)

        # remove node from adjacencies
        self.adj.pop(n)

    def add_edge(self, u_node, v_node, **attr) -> None:
        self.adj[u_node][v_node].update(attr)

        # for undirected graph this line is commented out
        self.adj[v_node][u_node].update(attr)

    def remove_edge(self, u_node, v_node) -> None:
        self.adj[u_node].pop(v_node)

        # for undirected graph this line is commented out
        self.adj[v_node].pop(u_node)

    def update(self, edges=None, nodes=None):
        pass

    def clear(self) -> None:
        pass

    def __iter__(self):
        pass

    def has_node(self, n):
        pass

    def __contains__(self, n):
        pass

    def has_edge(self, u, v):
        pass

    def get_edge_data(self, u, v, default=None):
        pass

    def neighbors(self, n):
        pass

    def __getitem__(self, n):
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
