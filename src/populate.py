from graph_construction import *
from edge.models import Edge
from node.models import Node
from source.models import Source
from news.models import News

import pandas as pd
from django.contrib.auth.models import User

import networkx as nx

graph_path = "/home/loricelli/Desktop/small_text.graphml"
data_path = "/home/loricelli/Github/thesis-spinoff/data/definitive_all.pkl"

#extracts the existing graph from the platform

old_graph = nx.DiGraph()
for edge in Edge.objects.all():
    old_graph.add_edge(edge.tail.news.news_id,edge.head.news.news_id)

print("NewsGraph extracted!")




data = pd.read_pickle(data_path)
data.drop_duplicates(subset=['url'],inplace=True)
data = data.sort_values(by='publish_date')
data.reset_index(inplace=True,drop=True)


new_graph = prova_grafo(data,30000,30400)
nx.write_graphml(new_graph, "test.graphml")

for edge in list(new_graph.edges):
    if edge not in old_graph.edges:
        if not isinstance(edge[0],str):
            if edge[0] not in old_graph.nodes:
                news_1 = data.loc[edge[0]]
                try:
                    source_1 = Source.objects.get(name=news_1.source)
                    print("Source already present")
                except:
                    source_1 = Source.objects.create(name=news_1.source)
                    print("Source created")

                ne_1 = News.objects.create(news_id=edge[0],title=news_1.title,body=news_1.text,source=source_1,publish_date=news_1.publish_date.to_pydatetime())
                n1 = Node.objects.create(news=ne_1, color=new_graph.nodes[edge[0]]['color'])
            else:
                ne_1 = News.objects.get(news_id=edge[0])
                n1 = Node.objects.get(news=ne_1)


            if edge[1] not in old_graph.nodes:
                news_2 = data.loc[edge[1]]
                try:
                    source_2 = Source.objects.get(name=news_2.source)
                except:
                    source_2 = Source.objects.create(name=news_2.source)

                ne_2 = News.objects.create(news_id=edge[1],title=news_2.title,body=news_2.text,source=source_2,publish_date=news_2.publish_date.to_pydatetime())
                n2 = Node.objects.create(news=ne_2, color=new_graph.nodes[edge[1]]['color'])
            else:
                ne_2 = News.objects.get(news_id=edge[1])
                n2 = Node.objects.get(news=ne_2)


            new_added = Edge.objects.create(tail=n1,head=n2)
            old_graph.add_edge(new_added.tail.news.news_id,new_added.head.news.news_id)

print("Create Superadmin.")
user=User.objects.create_user('loricelli', password='1')
user.is_superuser=True
user.is_staff=True
user.save()
print("Done!")
print("Create User.")
user=User.objects.create_user('lorenzo', password='1')
user.save()
print("Done!")

