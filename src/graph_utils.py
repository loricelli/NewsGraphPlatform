import networkx as nx
from networkx import shortest_path

def dump_graph(edges,with_data=False):
    graph = nx.DiGraph()

    for edge in edges:
        if with_data:
            tail = edge.tail
            head = edge.head

            if not graph.has_node(tail.news.news_id):
                graph.add_node(tail.news.news_id,color=tail.color)

            if not graph.has_node(head.news.news_id):
                graph.add_node(head.news.news_id,color=head.color)

            graph.add_edge(edge.tail.news.news_id,edge.head.news.news_id,color=edge.color,stance=edge.stance)
        else:
            graph.add_edge(edge.tail.news.news_id,edge.head.news.news_id)

    return graph


def to_analyze(wcc,nodes,graph):
    ret = list()

    for node in nodes:
        for cc in wcc:
            if node in cc:
                unseen_nodes = [x for x,y in graph.subgraph(cc).nodes(data=True) if y['color']=='violet']
                if not unseen_nodes and cc not in ret:
                    ret.append(cc)
                    break
    return ret

def same_color_nodes(graph,node,color):
    subgraph = nx.descendants(graph,node)
    same = list()
    for n in subgraph:
        if graph.nodes[n]['color'] in color:
            same.append(n)
    return same

confirm_color = "#196b0e"
self_disagree_color = "#fa7b0c"
disagree_color = "#bf0404"




def compute_tv(graph,node,color):
    scn = same_color_nodes(graph,node,color)
    desc = nx.descendants(graph,node)
    desc.add(node)
    subgraph = graph.subgraph(list(desc))
    tv = 0.0
    if scn:
        for n in scn:
            in_edges = subgraph.in_edges(n)
            for edge in in_edges:
                data = subgraph.get_edge_data(edge[0],edge[1])
                if data['color'] in [confirm_color,self_disagree_color,disagree_color]:
                    d = len(shortest_path(subgraph,node,edge[0]))
                    tv += 1/d
        if tv == 0.0:
            return tv,False
        else:
            return tv, True
    else:
        in_edges = subgraph.in_edges(node)

        if in_edges:
            #nodo finale
            for edge in in_edges:
                data = subgraph.get_edge_data(edge[0],edge[1])
                if data['color'] not in [confirm_color,self_disagree_color,disagree_color]:
                    return tv,False
            return tv,True
        else:
            #nodo iniziale che introduce la news
            in_edges = graph.in_edges(node)
            for edge in in_edges:
                data = graph.get_edge_data(edge[0],edge[1])
                if data['color'] not in [confirm_color,self_disagree_color,disagree_color]:
                    return tv,False
            return tv,True



def compute_tv_rebuild(graph,node,color):
    scn = same_color_nodes(graph,node,color)
    desc = nx.descendants(graph,node)
    desc.add(node)
    subgraph = graph.subgraph(list(desc))
    tv = 0.0
    if scn:
        for n in scn:
            in_edges = subgraph.in_edges(n)
            for edge in in_edges:
                data = subgraph.get_edge_data(edge[0],edge[1])
                if data['color'] in [confirm_color,self_disagree_color,disagree_color]:
                    d = len(shortest_path(subgraph,node,edge[0]))
                    tv += 1/d
        if tv == 0.0:
            #all nodes were linked trough invalid edges
            return tv,False
        else:
            return tv, True

    else: #no same color nodes. It may be true or it may be an end node
        if not subgraph.out_edges(node):
            #it is an end node
            #we check if its in_edges are valid. It may be only a dead end with an invalid edge.
            in_edges = graph.in_edges(node)
            for edge in in_edges:
                data = graph.get_edge_data(edge[0],edge[1])
                if data['color'] not in [confirm_color,self_disagree_color,disagree_color]:
                    return tv,False
            return tv,True
        else:
            return tv,True
        # else:





def explore_news_topic(subgraph):
    tv_table_pos = dict()
    tv_table_neg = dict()
    tv_table_zero= dict()
    for node in subgraph.nodes:
        node_color = subgraph.nodes[node]['color']

        same_col = ['green','white'] if node_color in ['green','white'] else ['black','yellow']
        diff_col = ['green','white'] if node_color in ['black','yellow'] else ['black','yellow']

        tv_p,valid_p = compute_tv_rebuild(subgraph,node,same_col)
        tv_n,valid_n = compute_tv_rebuild(subgraph,node,diff_col)
        tv = round((tv_p - tv_n),2)
        print("Node:",node,"tv_p",tv_p,"tv_n:",tv_n,"tv:",tv,valid_p,valid_n)

        if valid_p or valid_n:
            if tv == 0:
                tv_table_zero[node] = tv
            elif tv > 0:
                tv_table_pos[node] = tv
            else:
                tv_table_neg[node] = tv

    return tv_table_pos, tv_table_zero,tv_table_neg


def get_color_list(subgraph,tv_keys):
    colors = list()
    for key in tv_keys:
        if subgraph.nodes[key]['color'] in ['green','white']:
            colors.append('white')
        elif subgraph.nodes[key]['color'] in ['yellow','black']:
            colors.append('black')

    return colors


from collections import Counter

#return a pair real_news_color, fake_news_color
def get_real_fake_colors(subgraph,tv_pos,tv_zero,tv_neg):
    #Tries positive band at first
    tv_pos_colors = get_color_list(subgraph,tv_pos)
    tp_counter = Counter(tv_pos_colors)
    if tp_counter['black'] > tp_counter['white']:
        return 'black','white'
    elif tp_counter['black'] < tp_counter['white']:
        return 'white','black'

    elif tp_counter['black'] == tp_counter['white']:
        #positive band wasn't enough, let's try with the negative to find the fake news
        tv_neg_colors = get_color_list(subgraph,tv_neg)
        tp_counter = Counter(tv_neg_colors)
        #the most common in the negative band is the fake news, so the return values are reversed
        if tp_counter['black'] > tp_counter['white']:
            return 'white','black'
        elif tp_counter['black'] < tp_counter['white']:
            return 'black','white'

        elif tp_counter['black'] == tp_counter['white']:
            tv_zero_colors = get_color_list(subgraph,tv_zero)
            tp_counter = Counter(tv_zero_colors)

            if tp_counter['black'] > tp_counter['white']:
                return 'black','white'
            elif tp_counter['black'] < tp_counter['white']:
                return 'white','black'
            else:
                return 'draw','draw'



