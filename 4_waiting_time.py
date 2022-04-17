import pandas as pd
import numpy as np

def get_news_data():
    real_news = pd.read_csv("data/derived/real_news.csv")
    fake_news = pd.read_csv("data/derived/fake_news.csv")

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
    total_avg_wait_time = 0
    valid_users = 0

    for user in users:
        user_data = df.loc[df['user_screen_name'] == user]
        if user_data.shape[0] > 1:
            valid_users += 1
            user_data = user_data.sort_values(by=['created_at'])
            avg_wait_time = get_avg_waiting_time(user_data)
            print("Average wait time for {}: {} days".format(user, avg_wait_time))
            total_avg_wait_time += avg_wait_time

    print("Overall average wait time: {} days".format(total_avg_wait_time/valid_users))

if __name__ == '__main__':
    real_news_data, fake_news_data = get_news_data()
    distinct_real_news_users = real_news_data['user_screen_name'].unique()
    distinct_fake_news_users = fake_news_data['user_screen_name'].unique()

    all_news_data = pd.read_excel(open('data/twitter_fakenews_USElections_2016.xlsx', 'rb'), sheet_name='DATA')
    all_news_data['created_at'] = pd.to_datetime(all_news_data['created_at'])

    print("---------------- Real news users ----------------")
    print_avg_waiting_times(all_news_data, distinct_real_news_users)

    print("\n\n---------------- Fake news users ----------------")
    print_avg_waiting_times(all_news_data, distinct_fake_news_users)

"""
Result:
Overall average wait times
    Real news users = 32.46 days
    Fake news users = 22.9 days
"""