from graph_utils import *
from edge.models import Edge
from node.models import Node
from networkx.algorithms.components import weakly_connected_components
from datetime import datetime,timedelta


white_nodes = ['white','green']
black_nodes = ['black','yellow']

graph = dump_graph(Edge.objects.all(),True)


now = datetime.now()
day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
day_end = day_start + timedelta(hours=24)

nodes = Node.objects.filter(last_updated__gte=day_start,last_updated__lte=day_end)

node_list = [node.news.news_id for node in nodes]

#all news clusters
wcc = weakly_connected_components(graph)

components = to_analyze(list(wcc),node_list,graph)
print("COMPONENTS:",components)

for c in components:
    subgraph = graph.subgraph(c)
    tv_pos,tv_zero,tv_neg = explore_news_topic(subgraph)
    all_tvs = {**tv_pos,**tv_zero,**tv_neg}
    tv_pos_sort = sorted(tv_pos, key=tv_pos.get, reverse=True)
    tv_neg_sort = sorted(tv_neg, key=tv_neg.get, reverse=True)
    tv_zero_sort = sorted(tv_zero, key=tv_zero.get, reverse=True)
    # print(tv_pos_sort,tv_neg_sort,tv_zero_sort)

    for tv in all_tvs:
        node = Node.objects.get(news__news_id=tv)
        old_tv = node.truth_value
        new_tv = all_tvs[tv]
        node.truth_value = new_tv
        node.save()

        node.news.source.reliability += new_tv - old_tv
        node.news.source.save()


    if len(tv_pos_sort + tv_zero_sort + tv_neg_sort) > 1:
        real_color,fake_color = get_real_fake_colors(subgraph,tv_pos_sort,tv_zero_sort,tv_neg_sort)
        print("The",real_color,"news are True, while the",fake_color,"are fake news")

        if real_color == 'black':
            winner = black_nodes
        else:
            winner = white_nodes

        for node in c:
            to_update = Node.objects.get(news__news_id=node)
            if to_update.color in winner:
                to_update.fake = False
            else:
                to_update.fake = True
            to_update.save()

    else:
        print("Too few news!")





