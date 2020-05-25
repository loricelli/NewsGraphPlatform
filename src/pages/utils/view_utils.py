from collections import Counter
import networkx as nx

def get_fake_news(graph):
    topic_nodes = [node for node in graph.nodes if not graph.in_edges(node)]
    fake_news = []
    for node in topic_nodes:

        descendants = [graph.nodes[el]['color'] for el in nx.descendants(graph,node)]
        descendants.append(graph.nodes[node]['color'])
        c = Counter(descendants)

        if c['white'] > c['black']:
            fake_news.append((graph.nodes[node]['title'],c['black'],c['white'], c['black'] + c['white']))

    return fake_news

def get_graph(edges):
    graph = nx.DiGraph()
    for edge in edges:
        graph.add_node(edge.tail.news.news_id,color=edge.tail.color,title=edge.tail.news.title)
        graph.add_node(edge.head.news.news_id,color=edge.head.color,title=edge.head.news.title)
        graph.add_edge(edge.tail.news.news_id,edge.head.news.news_id,color=edge.color,stance=edge.stance)
    return graph


