from collections import OrderedDict


class mynetwork():
    def __init__(self) -> None:
        self.adj = {}
        self.attributes = {}

    def add_node(self, new_node, **attr) -> None:
        pass

    def remove_node(self, n) -> None:
        pass

    def add_edge(self, u_node, v_node, **attr) -> None:
        pass

    def remove_edge(self, u_node, v_node) -> None:
        pass

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
