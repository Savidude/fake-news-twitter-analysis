import pandas as pd
import re

import networkx as nx
import matplotlib.pyplot as plt

def get_news_data():
    real_news = pd.read_csv("data/derived/real_news.csv")
    fake_news = pd.read_csv("data/derived/fake_news.csv")

    return real_news, fake_news

def get_mentions(df):
    all_mentions = []
    for index, row in df.iterrows():
        tweet = row['text']
        user = row['user_screen_name']

        mentions = re.findall("(?<![@\w])@(\w{1,25})", tweet)
        if len(mentions) > 0:
            all_mentions.append((user, mentions))
    return all_mentions

def get_nodes(all_mentions):
    nodes = []
    for m in all_mentions:
        user = m[0]
        mentions = m[1]

        nodes.append(user)
        nodes.extend(mentions)

    return list(set(nodes)) # removes duplicate entries

def draw_graph(all_mentions):
    G = nx.Graph()

    nodes = get_nodes(all_mentions)
    G.add_nodes_from(nodes)

    for m in all_mentions:
        user = m[0]
        mentions = m[1]

        for mention in mentions:
            if mention != user:
                G.add_edge(user, mention)

    nx.draw_networkx(G)
    plt.show()

if __name__ == '__main__':
    real_news_data, fake_news_data = get_news_data()

    # real_news_mentions = get_mentions(real_news_data)
    # # draw_graph(real_news_mentions)

    fake_news_mentions = get_mentions(fake_news_data)
    draw_graph(fake_news_mentions)
