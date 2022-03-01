import turtle


class NodeView:

    def __init__(self, nodes):
        self._nodes = dict(nodes)

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

    def __str__(self):
        return str(list(self.items()))

    def __repr__(self) -> str:
        return f'NodeView({str(self)})'


class EdgeView:
    def __init__(self, edges):
        self._edges = {}
        for e in edges:
            if len(e) == 2:
                self._edges[e] = {}
            elif len(e) > 2:
                self._edges[(e[0], e[1])] = dict(e[2])

    def __getitem__(self, n):
        edge = self._edges.get(n)
        if not edge:
            edge = self._edges.get((n[1], n[0]))
        return edge

    def edgelist(self):
        edgelist = []
        for k, v in self._edges.items():
            edgelist.append((*k, v))
        return edgelist

    def __iter__(self):
        return iter(self.edgelist())

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

    def __str__(self):
        return str(self.edgelist())

    def __repr__(self) -> str:
        return f'EdgeView({str(self)})'


class mynetwork():
    """
    Mimic implementation of an undirected graph data structure from the networkx package. Nodes and edges can be assigned key-value attributes.
    """

    def __init__(self, edges=None, nodes=None):
        self._adj = {}
        self.attributes = {}

        if edges:
            self.update(edges, nodes)

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
                self.add_edges_from(edges)
            if nodes:
                self.add_nodes_from(nodes)
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
        try:
            return self._adj[u][v]
        except KeyError:
            return default

    def neighbors(self, n):
        return self._adj

    def adjacency(self):
        return self._adj

    def nbunch_iter(self, nbunch=None):

        pass

    def order(self):
        return len(self._adj)

    def number_of_nodes(self):
        return len(self._adj)

    def __len__(self):
        len(self._adj)

    def size(self):
        len(self._adj)

    def number_of_edges(self, u=None, v=None) -> int:
        return len(self._edges())

    def _edges(self):
        """
        Returns a dictionary of edges where the key is (u, v) with u > v, and the value is a dict of the edge attributes.
        """
        edge_set = set()
        edges = []
        for u, nbrs in self._adj.items():
            for v, attrs in nbrs.items():
                key = [u, v]
                key.sort()
                key = tuple(key)
                if key not in edge_set:
                    edge_set.add(tuple(key))
                    edges.append(tuple([*key, attrs]))

        return edges

    def __getattribute__(self, __name: str):
        if __name == 'nodes':
            return NodeView(list(self.attributes.items()))
        if __name == 'edges':
            return EdgeView(list(self._edges().items()))
        return object.__getattribute__(self, __name)

    def __str__(self):
        return f'Undirected graph with {self.number_of_nodes()} nodes and {self.number_of_edges()} edges.'

    def __repr__(self):
        return f'mynetwork(edges={list(self._edges())}, nodes={list(self.attributes.items())})'


def draw_graph(graph, pos=None):
    """
    Plots out the graph. This implementation uses the built-in turtle module of python.

    graph: a mynetwork object to plot out.
    pos: a dictionary of positions where each node of graph is a key to a tuple with (x, y). If no pos is passed, pos will be taken from the node attributes, with a default of (0, 0)
    """
    mindim = 1000000
    maxdim = 0
    turtle.mode('world')
    turtle.speed(0)
    turtle.pen(pensize=3)
    nodes = graph.nodes
    edges = graph.edges
    if not pos:
        pos = nodes.data('pos', default=(0, 0))
    for n, attr in nodes:
        margin = 100
        node_pos = pos[n]
        if node_pos[0] - margin < mindim:
            mindim = node_pos[0] - margin
        if node_pos[1] - margin < mindim:
            mindim = node_pos[1] - margin
        if node_pos[0] + margin > maxdim:
            maxdim = node_pos[0] + margin
        if node_pos[1] + margin > maxdim:
            maxdim = node_pos[1] + margin

    turtle.setworldcoordinates(mindim, mindim, maxdim, maxdim)
    for n, attr in nodes:
        radius = 20
        fontsize = radius
        node_pos = pos[n]
        turtle.penup()
        turtle.setpos(node_pos[0], node_pos[1]-radius)
        turtle.pendown()
        turtle.circle(radius=radius)
        turtle.penup()
        turtle.setpos(node_pos[0], node_pos[1] - fontsize/3)
        turtle.write(n, align='center', font=('Arial', fontsize, 'normal'))

    for e in edges:
        radius = 20
        u = e[0]
        v = e[1]
        turtle.penup()
        turtle.setpos(*pos[u])
        turtle.setheading(turtle.towards(*pos[v]))
        turtle.forward(radius)
        turtle.pendown()
        turtle.forward(turtle.distance(*pos[v])-radius)
    turtle.hideturtle()
    turtle.done()
