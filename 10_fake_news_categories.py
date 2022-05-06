import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re

def get_user_categories(df, users):
    categories = {}

    for user in users:
        user_data = df.loc[df['user_screen_name'] == user]

        category_1_values = user_data['fake_news_category_1'].values.tolist()
        category_2_values = user_data['fake_news_category_2'].values.tolist()
        category_values = category_1_values + category_2_values
        user_category = max(set(category_values), key=category_values.count)
        categories[user] = user_category

    return categories

def get_mentions(df):
    all_mentions = []
    for index, row in df.iterrows():
        tweet = row['text']
        user = row['user_screen_name']

        mentions = re.findall("(?<![@\w])@(\w{1,25})", tweet)
        if len(mentions) > 0:
            all_mentions.append((user, mentions))
    return all_mentions

def draw_graph(mentions, user_categories):
    G = nx.Graph()
    G.add_nodes_from([-1, 0, 1, 2, 3, 4, 5])

    for m in mentions:
        user = m[0]
        mentions = m[1]

        for mention in mentions:
            if mention != user:
                if mention in user_categories:
                    user_category = user_categories[user]
                    mention_category = user_categories[mention]
                    G.add_edge(user_category, mention_category)

    nx.draw_networkx(G)
    plt.show()

df = pd.read_excel(open('data/twitter_fakenews_USElections_2016.xlsx', 'rb'), sheet_name='DATA')
users = df['user_screen_name'].unique()

user_categories = get_user_categories(df, users)
mentions = get_mentions(df)
draw_graph(mentions, user_categories)
