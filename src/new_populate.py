from graph_construction import *
from edge.models import Edge
from node.models import Node
from source.models import Source
from news.models import News
import copy
from datetime import datetime,timedelta,date

import pandas as pd
from django.contrib.auth.models import User

import networkx as nx

data_path = "INSERT_PATH_OF_PKL_SCRAPER"

N_DAYS = 4
TAIL_NODE = 0
HEAD_NODE = 1

#extracts the existing graph from the platform

old_graph = nx.DiGraph()
for node in Node.objects.all():
    old_graph.add_node(node.news.news_id)
for edge in Edge.objects.all():
    old_graph.add_edge(edge.tail.news.news_id,edge.head.news.news_id)
print("NewsGraph extracted!")


now = datetime.now()
today = date.today()
start_day = today - timedelta(N_DAYS)
start_time = datetime(start_day.year,start_day.month,start_day.day)

data = pd.read_pickle(data_path)
data.drop_duplicates(subset=['url'],inplace=True)
data = data.sort_values(by='publish_date')
data.reset_index(inplace=True,drop=True)

mask = (data['publish_date'] > start_time) & (data['publish_date'] <= now)
data = data[mask]


tmp_graph = copy.deepcopy(old_graph)
new_graph = prova_grafo(data,0,len(data))

for edge in list(new_graph.edges):
    if edge not in old_graph.edges:
    #check if edge was unrelated
        if not isinstance(edge[TAIL_NODE],str): #check if not undirected edge
            if edge[TAIL_NODE] in old_graph.nodes and edge[HEAD_NODE] in old_graph.nodes:
                #edge was deleted so they were unrelated
                continue
            if edge[TAIL_NODE] not in tmp_graph.nodes:
                news_1 = data.loc[edge[TAIL_NODE]]

                try:
                    source_1 = Source.objects.get(name=news_1.source)
                    print("Source already present")
                except:
                    source_1 = Source.objects.create(name=news_1.source)
                    print("Source created")

                ne_1 = News.objects.create(news_id=edge[TAIL_NODE],title=news_1.title,body=news_1.text,source=source_1,publish_date=news_1.publish_date.to_pydatetime())
                n1 = Node.objects.create(news=ne_1, color=new_graph.nodes[edge[TAIL_NODE]]['color'])
            else:
                ne_1 = News.objects.get(news_id=edge[TAIL_NODE])
                n1 = Node.objects.get(news=ne_1)

            if edge[HEAD_NODE] not in tmp_graph.nodes:
                news_2 = data.loc[edge[HEAD_NODE]]
                try:
                    source_2 = Source.objects.get(name=news_2.source)
                except:
                    source_2 = Source.objects.create(name=news_2.source)

                ne_2 = News.objects.create(news_id=edge[HEAD_NODE],title=news_2.title,body=news_2.text,source=source_2,publish_date=news_2.publish_date.to_pydatetime())
                n2 = Node.objects.create(news=ne_2, color=new_graph.nodes[edge[HEAD_NODE]]['color'])
            else:
                ne_2 = News.objects.get(news_id=edge[HEAD_NODE])
                n2 = Node.objects.get(news=ne_2)

            print("ADDED",edge[TAIL_NODE],edge[HEAD_NODE])
            new_added = Edge.objects.create(tail=n1,head=n2)
            tmp_graph.add_edge(new_added.tail.news.news_id,new_added.head.news.news_id)


try:
    user = User.objects.get(username='admin')
except:
    print("Create Superadmin.")
    user=User.objects.create_user('admin', password='password')
    user.is_superuser=True
    user.is_staff=True
    user.save()
    print("Done!")

