from edge.models import Edge
from node.models import Node
from source.models import Source
from news.models import News

import networkx as nx
import pandas as pd

graph_path = "/home/loricelli/Desktop/small_text.graphml"
data_path = "/home/loricelli/Github/thesis-spinoff/data/definitive_all.pkl"
data = pd.read_pickle(data_path)
data.drop_duplicates(subset=['url'],inplace=True)

data = data.sort_values(by='publish_date')
data.reset_index(inplace=True,drop=True)


data = data[31000:33000]
new_graph = nx.read_graphml(graph_path)


old_graph = nx.DiGraph()


from django.contrib.auth.models import User
user=User.objects.create_user('loricelli', password='1')
user.is_superuser=True
user.is_staff=True
user.save()
print("user creato")

for edge in Edge.objects.all():
    old_graph.add_edge(str(edge.tail.news.news_id),str(edge.head.news.news_id))

print(old_graph.edges)

for edge in list(new_graph.edges):
    if edge not in old_graph.edges:
        if edge[0].isdigit():
            if edge[0] not in old_graph.nodes:
                news_1 = data.loc[int(edge[0])]
                try:
                    source_1 = Source.objects.get(name=news_1.source)
                    print("Source created")
                except:
                    source_1 = Source.objects.create(name=news_1.source)
                    print("Source already present")

                ne_1 = News.objects.create(news_id=edge[0],title=news_1.title,body=news_1.text,source=source_1,publish_date=news_1.publish_date.to_pydatetime())
                n1 = Node.objects.create(news=ne_1, color=new_graph.nodes[edge[0]]['color'])
            else:
                ne_1 = News.objects.get(news_id=edge[0])
                n1 = Node.objects.get(news=ne_1)


            if edge[1] not in old_graph.nodes:
                news_2 = data.loc[int(edge[1])]
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
            old_graph.add_edge(str(new_added.tail.news.news_id),str(new_added.head.news.news_id))



