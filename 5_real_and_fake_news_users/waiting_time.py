import pandas as pd
import numpy as np

def get_user_avg_waiting_time(user_data):
    total_waiting_time = 0
    for idx in range(1, user_data.shape[0]):
        tweet_1_timestamp = user_data.iloc[[idx - 1]]['created_at'].values[0]
        tweet_2_timestamp = user_data.iloc[[idx]]['created_at'].values[0]

        time_days = (tweet_2_timestamp - tweet_1_timestamp)/np.timedelta64(1, 'D')
        total_waiting_time += time_days

    avg_waiting_time = total_waiting_time/(user_data.shape[0] - 1)
    return avg_waiting_time

def get_avg_waiting_time(df, users):
    total_avg_wait_time = 0
    valid_users = 0

    for user in users:
        user_data = df.loc[df['user_screen_name'] == user]
        if user_data.shape[0] > 1:
            valid_users += 1
            user_data = user_data.sort_values(by=['created_at'])
            avg_wait_time = get_user_avg_waiting_time(user_data)
            # print("Average wait time for {}: {} days".format(user, avg_wait_time))
            total_avg_wait_time += avg_wait_time

    return total_avg_wait_time/valid_users