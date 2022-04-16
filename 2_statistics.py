import pandas as pd

def get_news_data():
    real_news = pd.read_csv("data/derived/real_news.csv")
    real_news['created_at'] = pd.to_datetime(real_news['created_at'])

    fake_news = pd.read_csv("data/derived/fake_news.csv")
    fake_news['created_at'] = pd.to_datetime(fake_news['created_at'])

    return real_news, fake_news

def get_follower_favourite_count(df, user):
    user_data = df.loc[df['user_screen_name'] == user]

    # If there are multiple entries for the same user, get the followers and favourite count from the latest post
    latest_update = user_data.loc[user_data['created_at'].idxmax()]
    followers = latest_update['user_followers_count']
    favourites = latest_update['user_favourites_count']

    return followers, favourites

def get_user_data(df, users):
    user_data = []
    for user in users:
        followers, favourites = get_follower_favourite_count(df, user)
        user_data.append([user, followers, favourites])

    df = pd.DataFrame(user_data, columns=['user', 'followers', 'favourites'])
    return df

def calculate_statistics(user_data):
    mean = user_data[['followers', 'favourites']].mean()
    std = user_data[['followers', 'favourites']].std()
    kurtosis = user_data[['followers', 'favourites']].kurtosis()
    skew = user_data[['followers', 'favourites']].skew()

    return mean, std, kurtosis, skew

def print_statistics(user_data):
    mean, std, kurtosis, skew = calculate_statistics(user_data)
    data = [['mean', mean['followers'], mean['favourites']],
            ['std', std['followers'], std['favourites']],
            ['kurtosis', kurtosis['followers'], kurtosis['favourites']],
            ['skew', skew['followers'], skew['favourites']]]
    df = pd.DataFrame(data, columns=['calculus', 'followers', 'favourites'])
    print(df.to_string(index=False))

if __name__ == '__main__':
    real_news_data, fake_news_data = get_news_data()

    distinct_real_news_users = real_news_data['user_screen_name'].unique()
    distinct_fake_news_users = fake_news_data['user_screen_name'].unique()

    real_news_user_data = get_user_data(real_news_data, distinct_real_news_users)
    fake_news_user_data = get_user_data(fake_news_data, distinct_fake_news_users)

    print("---------------- Real news user statistics ----------------")
    print_statistics(real_news_user_data)

    print("\n\n---------------- Fake news user statistics ----------------")
    print_statistics(fake_news_user_data)

"""
Results:
---------------- Real news user statistics ----------------
calculus    followers   favourites
    mean 8.736879e+05 16290.573916
     std 4.528774e+06 42793.841284
kurtosis 1.689031e+02   107.377638
    skew 1.169951e+01     8.362971


---------------- Fake news user statistics ----------------
calculus    followers   favourites
    mean 8.603676e+05 19030.928021
     std 5.263047e+06 33730.336597
kurtosis 2.587248e+02     9.716432
    skew 1.507789e+01     2.852188
    
Conclusion:
The mean and standard deviation values for both classes' followers and favourites are similar.
However, there is a considerable difference when we consider the kurtosis and skew values between the classes.
Thus, we can conclude that it is possible to discriminate the two classes using these statistical data.
"""