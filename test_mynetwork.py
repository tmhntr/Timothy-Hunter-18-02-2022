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
    assert 'A' in g.adj


def test_remove_node():
    g = mynetwork()
    g.add_node('A')
    assert 'A' in g.adj
    g.remove_node('A')
    assert 'A' not in g.adj


def test_add_edge_with_existing_nodes():
    g = mynetwork()
    g.add_node('A')
    g.add_node('B')
    g.add_edge('A', 'B')

    print(g.adj['B'])
    assert 'A' in g.adj['B']
    assert 'B' in g.adj['A']


def test_add_edge_with_new_nodes():
    g = graph_with_edge('A', 'B')

    assert 'A' in g.adj['B']
    assert 'B' in g.adj['A']


def test_remove_edge():
    g = graph_with_edge('A', 'B')
    g.remove_edge('A', 'B')

    assert 'A' not in g.adj['B']
    assert 'B' not in g.adj['A']
