from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import csv
from csv import DictWriter
import plotly.express as px
import pandas as pd

col_list = ["user_screen_name", "text"]

# reading datasets
fake_df = pd.read_csv("data/derived/fake_news.csv", usecols=col_list)
fake_df = fake_df.reset_index()
real_df = pd.read_csv("data/derived/real_news.csv", usecols=col_list)
real_df = real_df.reset_index()

analyzer = SentimentIntensityAnalyzer()
sentiments = ['user_screen_name', 'pos', 'neu', 'neg', 'compound']

# performing sentiment analysis for fake dataset and writing it into csv
with open('data/derived/fake_sentiment.csv', 'w', newline='') as csvfile:
    data = csv.writer(csvfile)
    data.writerow(['user_screen_name', 'pos', 'neu', 'neg', 'compound'])
    for index, row in fake_df.iterrows():
        fake_vs = analyzer.polarity_scores(row['text'])
        fake_vs['user_screen_name'] = row['user_screen_name']
        dictwriter_object = DictWriter(csvfile, fieldnames=sentiments, lineterminator='\n')
        dictwriter_object.writerow(fake_vs)
    csvfile.close()

#performing sentiment analysis for fake dataset and writing it into csv
with open('data/derived/real_sentiment.csv', 'w', newline='') as csvfile:
    data = csv.writer(csvfile)
    data.writerow(['user_screen_name', 'pos', 'neu', 'neg', 'compound'])
    for index, row in real_df.iterrows():
        real_vs = analyzer.polarity_scores(row['text'])
        real_vs['user_screen_name'] = row['user_screen_name']
        dictwriter_object = DictWriter(csvfile, fieldnames=sentiments, lineterminator='\n')
        dictwriter_object.writerow(real_vs)
    csvfile.close()

#reading fake sentiments and user names
df_fake_sentiments = pd.read_csv('data/derived/fake_sentiment.csv')
df_fake_sentiments = df_fake_sentiments.sort_values(['user_screen_name'])
df_fake_sentiments = df_fake_sentiments.reset_index(drop=True)
user_names = df_fake_sentiments['user_screen_name']

pos = df_fake_sentiments['pos']
neu = df_fake_sentiments['neu']
neg = df_fake_sentiments['neg']
n = len(df_fake_sentiments.index)

user_name = user_names[0]
pos_score = 0
neu_score = 0
neg_score = 0
fake_added = pd.DataFrame()
ind = 0

# adding and normalizing sentiment scores for each user name
for x in range(n):
    if user_name == user_names[x]:
        pos_score = pos_score + pos[x]
        neu_score = neu_score + neu[x]
        neg_score = neg_score + neg[x]
        continue
    else:
        # normalizing the sum of sentiments to 1
        sum = pos_score + neu_score + neg_score
        pos_score = pos_score / sum
        neu_score = neu_score / sum
        neg_score = neg_score / sum
        d = {'user_screen_name': user_name, 'pos': pos_score, 'neu': neu_score, 'neg': neg_score}
        fake_added = fake_added.append(d, ignore_index=True)
        user_name = user_names[x]
        pos_score = pos[x]
        neu_score = neu[x]
        neg_score = neg[x]

#reading real sentiments and user names
df_real_sentiments = pd.read_csv('data/derived/real_sentiment.csv')
df_real_sentiments = df_real_sentiments.sort_values(['user_screen_name'])
df_real_sentiments = df_real_sentiments.reset_index(drop=True)
user_names = df_real_sentiments['user_screen_name']

pos = df_real_sentiments['pos']
neu = df_real_sentiments['neu']
neg = df_real_sentiments['neg']
n = len(df_real_sentiments.index)

user_name = user_names[0]
pos_score = 0
neu_score = 0
neg_score = 0
real_added = pd.DataFrame()
ind = 0

# adding and normalizing sentiment scores for each user name
for x in range(n):
    if user_name == user_names[x]:
        pos_score = pos_score + pos[x]
        neu_score = neu_score + neu[x]
        neg_score = neg_score + neg[x]
        continue
    else:
        # normalizing the sum of sentiments to 1
        sum = pos_score + neu_score + neg_score
        pos_score = pos_score / sum
        neu_score = neu_score / sum
        neg_score = neg_score / sum
        d = {'user_screen_name': user_name, 'pos': pos_score, 'neu': neu_score, 'neg': neg_score}
        real_added = real_added.append(d, ignore_index=True)
        user_name = user_names[x]
        pos_score = pos[x]
        neu_score = neu[x]
        neg_score = neg[x]

# plotting fake ternary
fake_fig = px.scatter_ternary(fake_added, a="pos", b="neu", c="neg", labels={"neu": "Neutral",
                                 "pos": "Positive",
                                 "neg": "Negative"}, template="ggplot2") 
fake_fig.show()

# plotting real ternary
real_fig = px.scatter_ternary(real_added, a="pos", b="neu", c="neg", labels={"neu": "Neutral",
                                 "pos": "Positive",
                                 "neg": "Negative"}, template="ggplot2") 
real_fig.show()