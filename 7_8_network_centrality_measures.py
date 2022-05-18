#!/usr/bin/env python
# coding: utf-8

# In[1]:


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

    return list(set(nodes))  # removes duplicate entries


def get_graph(all_mentions):
    G = nx.Graph()

    nodes = get_nodes(all_mentions)
    G.add_nodes_from(nodes)

    for m in all_mentions:
        user = m[0]
        mentions = m[1]

        for mention in mentions:
            if mention != user:
                G.add_edge(user, mention)

    return G


if __name__ == '__main__':
    real_news_data, fake_news_data = get_news_data()

    real_news_mentions = get_mentions(real_news_data)
    G1 = get_graph(real_news_mentions)

    fake_news_mentions = get_mentions(fake_news_data)
    G2 = get_graph(fake_news_mentions)

    print(
        f"There are {G1.number_of_nodes()} nodes and {G1.number_of_edges()} edges present in the Graph for real news mentions")

    print(
        f"There are {G2.number_of_nodes()} nodes and {G2.number_of_edges()} edges present in the Graph for fake news mentions")

# In[2]:


if nx.is_connected(G1):
    print("The real news graph is connected")
else:
    print("The real news graph is not connected")

# In[3]:


if nx.is_connected(G2):
    print("The fake news graph is connected")
else:
    print("The fake news graph is not connected")

# In[49]:


print(f"There are {nx.number_connected_components(G1)} connected components in the real news Graph")

# In[50]:


print(f"There are {nx.number_connected_components(G2)} connected components in the fake news Graph")

# In[51]:


(G1.subgraph(c) for c in nx.connected_components(G1))
largestsubgraph1 = max((G1.subgraph(c) for c in nx.connected_components(G1)), key=len)
print("There are " + str(largestsubgraph1.number_of_nodes()) + " nodes and " + str(
    largestsubgraph1.number_of_edges()) + " edges present in the largest component of the real news graph.")

# In[52]:


(G2.subgraph(c) for c in nx.connected_components(G2))
largestsubgraph2 = max((G2.subgraph(c) for c in nx.connected_components(G2)), key=len)
print("There are " + str(largestsubgraph2.number_of_nodes()) + " nodes and " + str(
    largestsubgraph2.number_of_edges()) + " edges present in the largest component of the fake news graph.")

# In[53]:


if nx.is_connected(largestsubgraph1):
    print("The graph is connected")
else:
    print("The graph is not connected")

# In[54]:


if nx.is_connected(largestsubgraph2):
    print("The graph is connected")
else:
    print("The graph is not connected")

# In[55]:


nx.diameter(largestsubgraph1)

# In[56]:


nx.diameter(largestsubgraph2)

# In[57]:


nx.cluster.average_clustering(largestsubgraph1)

# In[13]:


nx.cluster.average_clustering(largestsubgraph2)

# In[19]:


# plt.hist(nx.cluster.average_clustering(largestsubgraph1))
# plt.savefig("Average Clustering Coefficient distribution for real news dataset.png")


# In[20]:


# plt.hist(nx.cluster.average_clustering(largestsubgraph2))
# plt.savefig("Average Clustering Coefficient distribution for fake news dataset.png")


# In[58]:


bc = nx.centrality.betweenness_centrality(largestsubgraph1)
avg_bc = sum(bc.values()) / len(bc)
print(avg_bc)

bc2 = nx.centrality.betweenness_centrality(largestsubgraph2)
avg_bc2 = sum(bc2.values()) / len(bc2)
print(avg_bc2)

# In[59]:


cc1 = nx.centrality.closeness_centrality(largestsubgraph1)
avg_cc1 = sum(cc1.values()) / len(cc1)
print(avg_cc1)

cc2 = nx.centrality.closeness_centrality(largestsubgraph2)
avg_cc2 = sum(cc2.values()) / len(cc2)
print(avg_cc2)

# In[23]:


nx.centrality.closeness_centrality(largestsubgraph2)

# In[60]:


dc1 = nx.degree_centrality(largestsubgraph1)

avg_dc1 = sum(dc1.values()) / len(dc1)
print(avg_dc1)

dc2 = nx.degree_centrality(largestsubgraph2)

avg_dc2 = sum(dc2.values()) / len(dc2)
print(avg_dc2)

# In[31]:


degree_sequence1 = sorted([d for n, d in largestsubgraph1.degree()], reverse=True)
print(degree_sequence1)

# In[61]:


plt.hist(degree_sequence1)
plt.title("Degree_Centrality_Distribution_RealNews")
plt.savefig("Degree_Centrality_Distribution_RealNews.png")

# In[62]:


degree_sequence2 = sorted([d for n, d in largestsubgraph2.degree()], reverse=True)
print(degree_sequence2)
plt.title("Degree_Centrality_Distribution_Fake News")
plt.hist(degree_sequence2)

plt.savefig("Degree_Centrality_Distribution_FakeNews.png")

# In[63]:


cc1 = list(nx.clustering(largestsubgraph1).values())
print(cc1)
plt.title("Clustering_coefficient_Distribution_cc1")
plt.hist(cc1)
plt.savefig("Clustering_coefficient_Distribution_cc1.png")

# In[64]:


cc2 = list(nx.clustering(largestsubgraph2).values())
print(cc2)
plt.title("Clustering_coefficient_Distribution_cc2")
plt.hist(cc2)
plt.savefig("Clustering_coefficient_Distribution_cc2.png")
