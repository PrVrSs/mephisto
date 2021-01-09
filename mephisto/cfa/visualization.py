from typing import List, Tuple

import networkx
from matplotlib import pyplot


def visualize(edges: List[Tuple[int, int]]) -> None:
    options = {
        'node_color': 'red',
        'node_size': 600,
        'width': 1.5,
        'arrowsize': 12,
    }

    graph = networkx.DiGraph(direct=True)
    graph.add_edges_from(edges)
    networkx.draw_networkx(graph, **options)
    pyplot.show()
