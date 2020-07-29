import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import RegexpTokenizer
import networkx as nx

import matplotlib.pyplot as plt

import numpy as np
import spacy
from networkx.classes.function import is_empty
from networkx.algorithms import topological_sort

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

nlp = spacy.load('en_core_web_lg')

from datetime import datetime


to_clean_sents = ['Sign up',"newsletter",'Subscribe to',"FILE PHOTO", "Click","Photo","Image copyright","Guide"]
to_clean_urls = ['gallery','videos','michigansbest','lifestyle']
to_clean_titles = ["?","!","Best","How to","Live Update"]

PERCENTAGE = 0.45

def jaccard(a, b):
    c = a.intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))

def valid_item(text,to_clean_list):
  if any(ext in text for ext in to_clean_list):
    return False
  elif to_clean_list == to_clean_sents:
    return not text.isupper()
  else:
    return True

def custom_get_sents(text):
  sents = []
  for sent in nltk.sent_tokenize(text):
      if valid_item(sent,to_clean_sents) and not sent.islower() and not sent.isupper():
          sents.append(sent)
  return sents

def common_ents(set_ents_1,set_ents_2):
  common = set_ents_1.intersection(set_ents_2)
  set_union = set_ents_1.union(set_ents_2)
  tot = len(set_union)

  if tot == 0:
    return set()
  else:
    return common

def get_ner_set(article):
  ents = [e.text for e in article.ents]
  set_ents = set(ents)
  return set_ents

def get_perc(common,s1,s2):
  if len(common) > 0:
    MAX = max(len(s1),len(s2))
    MIN = min(len(s1),len(s2))
    return jaccard(s1,s2)
  else:
    return 0

def compare_ners(ner_set,news_graph,to_insert):

  same_news_list = []
  node_list = [node for node in news_graph.nodes.data(data=True) if node[1]['type'] == 'news']

  for node in node_list:
    node_ner_set = set(node[1]['ner_set'].split(";"))
    common_set = common_ents(ner_set,node_ner_set)
    percentage = get_perc(common_set,ner_set,node_ner_set)

    if percentage > PERCENTAGE and len(common_set) > 3:
      same_news_list.append(node[0])
  return same_news_list

def get_edge_nodes(node_a,node_b,data):
    date_a = data.loc[node_a].publish_date
    date_b = data.loc[node_b].publish_date
    tail,head = (node_a,node_b) if date_a < date_b else (node_b,node_a)
    return tail,head

def insert_news(to_insert,graph,news):
  sents =  [sent for sent in custom_get_sents(to_insert.text)]
  text = " ".join(sents)
  text = " ".join(text.split()[:150])

  doc = nlp(text)
  ner_set = get_ner_set(doc)

  if to_insert.source == "www.suntimes.com":
    return graph
  if not graph.has_node(to_insert.source):
    graph.add_node(to_insert.source,type='source',color='#4383CC',size=10)

  same_news_list = compare_ners(ner_set,graph,to_insert)
  if not same_news_list:
    graph.add_node(to_insert.name,title=to_insert.title,ner_set=";".join(list(ner_set)), type='news',size=10,color='black')
    graph.add_edge(to_insert.source, to_insert.name,type='publish',color='#DCDCDC')
    return graph
  else:
    graph.add_node(to_insert.name,title=to_insert.title,ner_set=";".join(list(ner_set)), type='news',size=10,color='violet')
    for node in same_news_list:
      node_data = graph.nodes[node]
      tail,head = get_edge_nodes(to_insert.name,node,news)
      graph.add_edge(tail,head,type='match',color="black",stance=-1)
      graph.add_edge(to_insert.source, to_insert.name,type='publish',color='#DCDCDC')
  return graph




import networkx as nx

def prova_grafo(data,start,stop):
    news_graph = nx.DiGraph()
    for i in range(start,stop):
        to_insert = data.loc[i]
        if valid_item(to_insert.url,to_clean_urls) and valid_item(to_insert.title,to_clean_titles):
            news_graph = insert_news(to_insert,news_graph,data)

    print(len([edge for edge in news_graph.edges.data(data=True) if edge[2]['type'] == 'match']),"matches found")
    print(len(list(nx.simple_cycles(news_graph))), " cycles in the news_graph!")
    return news_graph
