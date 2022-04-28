import pandas as pd

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

def print_statistics(df, users):
    user_data = get_user_data(df, users)
    mean, std, kurtosis, skew = calculate_statistics(user_data)
    data = [['mean', mean['followers'], mean['favourites']],
            ['std', std['followers'], std['favourites']],
            ['kurtosis', kurtosis['followers'], kurtosis['favourites']],
            ['skew', skew['followers'], skew['favourites']]]
    df = pd.DataFrame(data, columns=['calculus', 'followers', 'favourites'])
    print(df.to_string(index=False))
