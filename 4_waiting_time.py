import pandas as pd
import numpy as np

def get_news_data():
    real_news = pd.read_csv("data/derived/real_news.csv")
    real_news['created_at'] = pd.to_datetime(real_news['created_at'])

    fake_news = pd.read_csv("data/derived/fake_news.csv")
    fake_news['created_at'] = pd.to_datetime(fake_news['created_at'])

    return real_news, fake_news

def get_avg_waiting_time(user_data):
    total_waiting_time = 0
    for idx in range(1, user_data.shape[0]):
        tweet_1_timestamp = user_data.iloc[[idx - 1]]['created_at'].values[0]
        tweet_2_timestamp = user_data.iloc[[idx]]['created_at'].values[0]

        time_days = (tweet_2_timestamp - tweet_1_timestamp)/np.timedelta64(1, 'D')
        total_waiting_time += time_days

    avg_waiting_time = total_waiting_time/(user_data.shape[0] - 1)
    return avg_waiting_time

def print_avg_waiting_times(df, users):
    for user in users:
        user_data = df.loc[df['user_screen_name'] == user]
        if user_data.shape[0] > 1:
            user_data = user_data.sort_values(by=['created_at'])
            avg_wait_time = get_avg_waiting_time(user_data)
            print("Average wait time for {}: {} days".format(user, avg_wait_time))

if __name__ == '__main__':
    real_news_data, fake_news_data = get_news_data()

    distinct_real_news_users = real_news_data['user_screen_name'].unique()
    distinct_fake_news_users = fake_news_data['user_screen_name'].unique()

    print("---------------- Real news users ----------------")
    print_avg_waiting_times(real_news_data, distinct_real_news_users)

    print("\n\n---------------- Fake news users ----------------")
    print_avg_waiting_times(fake_news_data, distinct_fake_news_users)