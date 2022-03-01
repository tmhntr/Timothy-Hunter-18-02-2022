from mynetwork import mynetwork

G = mynetwork()
nodes = [
    ('A', {}),
    ('B', {'pos': (200, 100)}),
    ('C', {'pos': (100, 200)}),
    ('D', {'pos': (200, 200)}),
    ('E', {'pos': (100, 300)}),
    ('F', {'pos': (200, 300)})
]
G.add_nodes_from(nodes)
edges = [
    ('A', 'B'),
    ('A', 'D'),
    ('E', 'F')
]
G.add_edges_from(edges)

print(repr(G))
