from mynetwork import mynetwork


def graph_with_edge(a, b):
    g = mynetwork()
    g.add_edge(a, b)

    return g


def test_create_mynetwork_object():
    g = mynetwork()


def test_add_node():
    g = mynetwork()
    g.add_node('A')
    assert 'A' in g


def test_remove_node():
    g = mynetwork()
    g.add_node('A')
    assert 'A' in g
    g.remove_node('A')
    assert 'A' not in g


def test_add_edge_with_existing_nodes():
    g = mynetwork()
    g.add_node('A')
    g.add_node('B')
    g.add_edge('A', 'B')

    assert 'A' in g['B']
    assert 'B' in g['A']


def test_add_edge_with_new_nodes():
    g = graph_with_edge('A', 'B')

    assert 'A' in g['B']
    assert 'B' in g['A']


def test_remove_edge():
    g = graph_with_edge('A', 'B')
    g.remove_edge('A', 'B')

    assert 'A' not in g['B']
    assert 'B' not in g['A']


def test_getitem_dunder_method():
    g = graph_with_edge('A', 'B')

    assert g['A'] == {'B': {}}


def test_contains_dunder_method():
    g = mynetwork()
    g.add_node('A')

    assert 'A' in g


def test_has_node():
    g = graph_with_edge('A', 'B')
    assert g.has_node('A')
    assert not g.has_node('C')


def test_has_edge():
    g = graph_with_edge('A', 'B')
    g.add_node('C')
    assert g.has_edge('A', 'B')
    assert not g.has_edge('A', 'C')


def test_update_with_edges():
    g = graph_with_edge('A', 'B')
    g.add_node('C')
    g.update(edges=[('B', 'C')])
    assert g.has_edge('B', 'C')


def test_update_with_edges():
    g = graph_with_edge('A', 'B')
    g.update(nodes={'C': {'A', 'B'}})
    assert g.has_node('C')


def test_add_nodes_from():
    g = mynetwork()
    g.add_nodes_from(['A', 'B'])
    assert g.has_node('A') and g.has_node('B')

    h = mynetwork()
    h.add_nodes_from([('A', {'data': 'mydata'}), ('B', {})], alldata='all')
    assert h.nodes['A']['data'] == 'mydata'
    assert h.nodes['A']['alldata'] == 'all' and h.nodes['B']['alldata'] == 'all'


def test_iter():
    g = mynetwork()
    g.add_nodes_from(['A', 'B'])
    it = iter(g)
    assert next(it) == 'A'
    assert next(it) == 'B'


def test_get_edges():
    g = mynetwork()
    nodes = ['A', 'B', 'C']
    g.add_nodes_from(nodes)
    for i in range(len(nodes)):
        g.add_edge(nodes[i], nodes[i-1], val=i+1)

    # print(g)
    assert g.edges == {
        ('A', 'C'): {'val': 1},
        ('A', 'B'): {'val': 2},
        ('B', 'C'): {'val': 3}
    }


def test_add_edges_from():
    g = mynetwork()
    nodes = ['A', 'B', 'C']
    edges = []
    g.add_nodes_from(nodes)
    for i in range(len(nodes)):
        edges.append((nodes[i], nodes[i-1], {'val': i+1}))
    g.add_edges_from(edges)
    assert g.edges == {
        ('A', 'C'): {'val': 1},
        ('A', 'B'): {'val': 2},
        ('B', 'C'): {'val': 3}
    }


def test_copy_by_nodes_and_edges():
    g = mynetwork()
    nodes = [('A', {'name': 'A'}), ('B', {'name': 'B'}), ('C', {'name': 'C'})]
    edges = []
    g.add_nodes_from(nodes)
    for i in range(len(nodes)):
        edges.append((nodes[i][0], nodes[i-1][0], {'val': i+1}))
    g.add_edges_from(edges)

    h = mynetwork()
    h.add_nodes_from(g.nodes)
    h.add_edges_from(g.edges)
    # h.update(g)
    assert h.edges == g.edges
    assert h.nodes == g.nodes
