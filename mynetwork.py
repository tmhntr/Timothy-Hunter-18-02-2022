class NodeView:

    def __init__(self, nodes):
        self._nodes = nodes

    def __getitem__(self, n):
        return self._nodes[n]

    def __iter__(self):
        nodelist = []
        for k, v in self._nodes.items():
            nodelist.append((k, v))
        return iter(nodelist)

    def __contains__(self, n):
        return n in self._nodes

    def __eq__(self, obj):
        return self._nodes == obj

    def items(self):
        return self._nodes.items()

    def data(self, data, default=None):
        if type(data) == bool and data:
            return self._nodes
        nodedata = {}
        for n, attr in self._nodes.items():
            nodedata[n] = attr.get(data) if attr.get(data) else default
        return nodedata


class EdgeView:
    def __init__(self, edges):
        self._edges = edges

    def __getitem__(self, n):
        edge = self._edges.get(n)
        if not edge:
            edge = self._edges.get((n[1], n[0]))
        return edge

    def __iter__(self):
        edgelist = []
        for k, v in self._edges.items():
            edgelist.append((*k, v))
        return iter(edgelist)

    def __contains__(self, n):
        return n in self._edges

    def __eq__(self, obj):
        return self._edges == obj

    def items(self):
        return self._edges.items()

    def data(self, data, default=None):
        if type(data) == bool and data:
            return self._edges
        nodedata = {}
        for n, attr in self._edges.items():
            nodedata[n] = attr.get(data) if attr.get(data) else default
        return nodedata

    def __call__(self, nbunch=False, data=False, default=None):
        if not data:
            return iter(self._edges)
        else:
            return iter(self.data(data, default).items())


class mynetwork():
    """
    Mimic implementation of an undirected graph data structure from the networkx package. Nodes and edges can be assigned key-value attributes. 
    """

    def __init__(self):
        self._adj = {}
        self.attributes = {}

    def add_node(self, new_node, **attr) -> None:
        """
        Add a new node to the graph. 

        new_node: any hashable object that will be used to identify the node. If the node already exists, the node will be updated with attributes from attr.
        attr: any keyword args will be assigned as attributes to the node.

        Raises ValueError if new_node is not hashable.
        """
        if (not hasattr(new_node, "__hash__")):
            raise ValueError(f"{new_node} is not a hashable object.")
        else:
            self._adj[new_node] = {}
            self.attributes[new_node] = {}
            # print(attr)
            for k, v in attr.items():
                self.attributes[new_node][k] = v

    def add_nodes_from(self, nodes_for_adding, **attr):
        """
        Add new nodes to the graph. 

        nodes_for_adding: If this is a collection of tuples, nodes will be added as if by -> for k, v in nodes_for_adding, else each value in nodes_for_ading will be added as a node.
        attr: keyword arguments will be added to each node in nodes_for_adding.

        Raises ValueError if node to add is not hashable.
        """
        for node in nodes_for_adding:
            if isinstance(node, tuple):
                node[1].update(attr)
                self.add_node(node[0], **node[1])
            else:
                for node in nodes_for_adding:
                    self.add_node(node, **attr)

    def remove_node(self, n) -> None:
        """
        Remove a node from the graph.

        n: node to be removed from the graph. This is the same hashable object that was used to add the node.
        """
        # Remove node from all node adjacencies
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
        """
        Add a connection between two nodes. If either of the nodes does not exist, they will be added.

        u_node: A reference to one of the nodes to be connected.
        v_node: A reference to one of the nodes to be connected.
        attr: keyword argumentw to be assigned as attributes to the edge.
        """
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

    def add_edges_from(self, ebunch_to_add, **attr):
        """
        Add a collection of edges to the graph.

        ebunch_to_add: A collection of edges as tuples to be added to the graph. If the tuple has 2 elements, they will be taken as (u, v). If the tuple has 3 elements, the elements will be taken as u, v, and a dict of attributes
        attr: keyword arguments to be added to all the edges as attributes. 
        """
        for e in ebunch_to_add:
            if len(e) <= 2:
                self.add_edge(*e, **attr)
            elif len(e) == 3:
                e[2].update(attr)
                self.add_edge(e[0], e[1], **e[2])

    def remove_edge(self, u_node, v_node) -> None:
        """
        Remove an edge from the graph.

        u_node: one node of the edge to remove
        v_node: one node of the edge to remove
        """
        self._adj[u_node].pop(v_node)
        # for undirected graph this line is commented out
        self._adj[v_node].pop(u_node)

    def update(self, edges=None, nodes=None):
        """
        Update the graph using another graph object,or a list of edges and/or nodes.

        edges: May be a mynetwork object, or a collection of edges to add. Default value is None
        nodes: A collection of nodes to add. Default value is None.
        """
        if hasattr(edges, 'nodes') and hasattr(edges, 'edges'):
            self.add_nodes_from(edges.nodes)
            self.add_edges_from(edges.edges)
        else:
            if edges:
                for e in edges:
                    self.add_edge(*e)
            if nodes:
                for n in nodes:
                    self.add_node(n)
            if not edges and not nodes:
                raise ValueError(
                    'Either edges or nodes must be passed a value')

    def clear(self) -> None:
        """
        Remove all edges and nodes from the graph.
        """
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

    def _edges(self):
        """
        Returns a dictionary of edges where the key is (u, v) with u > v, and the value is a dict of the edge attributes.
        """
        edge_dict = {}
        for u, nbrs in self._adj.items():
            for v, attrs in nbrs.items():
                key = [u, v]
                key.sort()
                key = tuple(key)
                if key not in edge_dict:
                    edge_dict[key] = attrs
        return edge_dict

    def __getattribute__(self, __name: str):
        if __name == 'nodes':
            return NodeView(self.attributes)
        if __name == 'edges':
            return EdgeView(self._edges())
        return object.__getattribute__(self, __name)
