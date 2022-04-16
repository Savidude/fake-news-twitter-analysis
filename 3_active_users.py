import pandas as pd

def get_news_data():
    real_news = pd.read_csv("data/derived/real_news.csv")
    real_news['created_at'] = pd.to_datetime(real_news['created_at'])

    fake_news = pd.read_csv("data/derived/fake_news.csv")
    fake_news['created_at'] = pd.to_datetime(fake_news['created_at'])

    return real_news, fake_news

def print_average_tweet_count(tweet_count, length):
    count_values = tweet_count[0:length]
    print("Average number of tweets for the {} most active users: {}".format(length, count_values.mean()))

if __name__ == '__main__':
    real_news_data, fake_news_data = get_news_data()

    real_news_user_tweet_count = real_news_data['user_screen_name'].value_counts()
    fake_news_user_tweet_count = fake_news_data['user_screen_name'].value_counts()

    print("---------------- Real news users ----------------")
    print_average_tweet_count(real_news_user_tweet_count, 3)
    print_average_tweet_count(real_news_user_tweet_count, 5)
    print_average_tweet_count(real_news_user_tweet_count, 10)
    print_average_tweet_count(real_news_user_tweet_count, 15)

    print("\n\n---------------- Fake news users ----------------")
    print_average_tweet_count(fake_news_user_tweet_count, 3)
    print_average_tweet_count(fake_news_user_tweet_count, 5)
    print_average_tweet_count(fake_news_user_tweet_count, 10)
    print_average_tweet_count(fake_news_user_tweet_count, 15)

"""
Result:
---------------- Real news users ----------------
Average number of tweets for the 3 most active users: 332.6666666666667
Average number of tweets for the 5 most active users: 257.2
Average number of tweets for the 10 most active users: 168.3
Average number of tweets for the 15 most active users: 132.66666666666666


---------------- Fake news users ----------------
Average number of tweets for the 3 most active users: 33.0
Average number of tweets for the 5 most active users: 25.2
Average number of tweets for the 10 most active users: 17.1
Average number of tweets for the 15 most active users: 13.666666666666666
"""