from graph_utils import *
from edge.models import Edge
from node.models import Node
from networkx.algorithms.components import weakly_connected_components

graph = dump_graph(Edge.objects.all(),True)

nodes = Node.objects.all()

node_list = [node.news.news_id for node in nodes]

#all news clusters
wcc = weakly_connected_components(graph)

components = to_analyze(list(wcc),node_list,graph)
print("COMPONENTS:",components)

for c in components:
    subgraph = graph.subgraph(c)
    tv_pos,tv_zero,tv_neg = explore_news_topic(subgraph)
    tv_pos_sort = sorted(tv_pos, key=tv_pos.get, reverse=True)
    tv_neg_sort = sorted(tv_neg, key=tv_neg.get, reverse=True)
    tv_zero_sort = sorted(tv_zero, key=tv_zero.get, reverse=True)
    # print(tv_pos_sort,tv_neg_sort,tv_zero_sort)

    if len(tv_pos_sort + tv_zero_sort + tv_neg_sort) > 1:
        real_color,fake_color = get_real_fake_colors(subgraph,tv_pos_sort,tv_zero_sort,tv_neg_sort)
        print("The",real_color,"news are True, while the",fake_color,"are fake news")
    else:
        print("Too few news!")





