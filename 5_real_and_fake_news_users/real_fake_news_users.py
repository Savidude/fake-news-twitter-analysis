import pandas as pd
import numpy as np

from statistics import print_statistics
from waiting_time import get_avg_waiting_time

def get_news_data():
    all_tweets = pd.read_excel(open('../data/twitter_fakenews_USElections_2016.xlsx', 'rb'), sheet_name='DATA')
    all_tweets['created_at'] = pd.to_datetime(all_tweets['created_at'])
    return all_tweets

def get_real_fake_news_data():
    real_news = pd.read_csv("../data/derived/real_news.csv")
    real_news['created_at'] = pd.to_datetime(real_news['created_at'])

    fake_news = pd.read_csv("../data/derived/fake_news.csv")
    fake_news['created_at'] = pd.to_datetime(fake_news['created_at'])

    return real_news, fake_news

def get_distinct_real_and_fake_news_users(real_news, fake_news):
    distinct_real_news_users = real_news['user_screen_name'].unique()
    distinct_fake_news_users = fake_news['user_screen_name'].unique()
    distinct_real_fake_news_users = np.intersect1d(distinct_real_news_users, distinct_fake_news_users)
    return distinct_real_fake_news_users

def get_real_fake_news_user_data(news_data, users):
    df = news_data[news_data['user_screen_name'].isin(users)]
    return df

"""
-------------------------- Functions to get active users --------------------------
"""
def print_average_tweet_count(tweet_count, length):
    count_values = tweet_count[0:length]
    print("Average number of tweets for the {} most active users: {}".format(length, count_values.mean()))

def print_user_tweet_counts(news_data):
    user_tweet_counts = news_data['user_screen_name'].value_counts()
    print_average_tweet_count(user_tweet_counts, 3)
    print_average_tweet_count(user_tweet_counts, 5)
    print_average_tweet_count(user_tweet_counts, 10)
    print_average_tweet_count(user_tweet_counts, 15)

if __name__ == '__main__':
    all_news_data = get_news_data()
    real_news_data, fake_news_data = get_real_fake_news_data()

    real_fake_news_users = get_distinct_real_and_fake_news_users(real_news_data, fake_news_data)
    print("----------------- user statistics -----------------")
    print_statistics(all_news_data, real_fake_news_users)
    print()

    real_fake_news_user_data = get_real_fake_news_user_data(all_news_data, real_fake_news_users)
    print("----------------- tweet counts for the most active users -----------------")
    print_user_tweet_counts(real_fake_news_user_data)
    print()

    print("Average waiting time: {}".format(get_avg_waiting_time(all_news_data, real_fake_news_users)))

"""
Result:
----------------- user statistics -----------------
calculus    followers   favourites
    mean 1.508315e+06 20569.533654
     std 7.178369e+06 37424.431639
kurtosis 1.370316e+02    10.281801
    skew 1.099879e+01     2.947757

----------------- tweet counts for the most active users -----------------
Average number of tweets for the 3 most active users: 357.3333333333333
Average number of tweets for the 5 most active users: 273.4
Average number of tweets for the 10 most active users: 178.9
Average number of tweets for the 15 most active users: 142.46666666666667

Average waiting time: 22.492744961735795
"""
