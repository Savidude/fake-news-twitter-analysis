import pandas as pd
import numpy as np

def is_fake_news(data):

    class_1 = data['is_fake_news_1']
    class_2 = data['is_fake_news_2']

    class_1_category = data['fake_news_category_1']
    class_2_category = data['fake_news_category_2']

    """
    if both classifications is 'UNKNOWN' we will consider this to be real news
    """
    if class_1 == 'UNKNOWN' and class_2 == 'UNKNOWN':
        return False

    """
    if one classification is 'UNKNOWN' and the other is 'FALSE', we will consider this to be real news
    """
    if (class_1 == 'UNKNOWN' and class_2 == False) or (class_1 == False and class_2 == 'UNKNOWN'):
        return False

    """
    if one classification is 'UNKNOWN' and the other is 'TRUE',
    this will be classified as
        fake news: if the TRUE classification has a category of 1 or 2
        real news: if the TRUE classification has a category of 3, 4, or 5
    """
    if class_1 == 'UNKNOWN' and class_2 == True:
        if class_2_category == 1 or class_2_category == 2:
            return True
        else:
            return False
    elif class_1 == True and class_2 == 'UNKNOWN':
        if class_1_category == 1 or class_1_category == 2:
            return True
        else:
            return False

    """
    if one classification is 'TRUE' and the other is 'FALSE',
    this will be classified as,
        fake_news:
            - if the FALSE classification is a category 0, and TRUE classification is category 1 or 2
            - if the FALSE classification is a category -1, and TRUE classification is category 1
        real_news:
            - if the FALSE classification is a category 0, and TRUE classification is category 3, 4, or 5
            - if the FALSE classification is a category -1, and TRUE classification is category 2, 3, 4, or 5
    """
    if class_1 == True and class_2 == False:
        if class_2_category == 0:
            if class_1_category == 1 or class_1_category == 2:
                return True
            else:
                return False
        elif class_2_category == -1:
            if class_1_category == 1:
                return True
            else:
                return False
    elif class_1 == False and class_2 == True:
        if class_1_category == 0:
            if class_2_category == 1 or class_2_category == 2:
                return True
            else:
                return False
        elif class_1_category == -1:
            if class_2_category == 1:
                return True
            else:
                return False

    return False

def classify_news_type(df):
    real_news = df.loc[(df['is_fake_news_1'] == False) & (df['is_fake_news_2'] == False)]
    fake_news = df.loc[(df['is_fake_news_1'] == True) & (df['is_fake_news_2'] == True)]

    conflicting_data = df.loc[df['is_fake_news_1'] != df['is_fake_news_2']]
    for index, row in conflicting_data.iterrows():
        if is_fake_news(row):
            fake_news = fake_news.append(row, ignore_index = True)
        else:
            real_news = real_news.append(row, ignore_index=True)

    return real_news, fake_news

def classify_and_write():
    df = pd.read_excel(open('data/twitter_fakenews_USElections_2016.xlsx', 'rb'), sheet_name='DATA')
    real_news_data, fake_news_data = classify_news_type(df)
    real_news_data.to_csv('data/derived/real_news.csv', index=False)
    fake_news_data.to_csv('data/derived/fake_news.csv', index=False)

def print_distinct_users():
    real_news_data = pd.read_csv("data/derived/real_news.csv")
    fake_news_data = pd.read_csv("data/derived/fake_news.csv")

    distinct_real_news_users = real_news_data['user_screen_name'].unique()
    distinct_fake_news_users = fake_news_data['user_screen_name'].unique()

    distinct_real_fake_news_users = np.intersect1d(distinct_real_news_users, distinct_fake_news_users)

    print("Distinct real news users: ", len(distinct_real_news_users))
    print("Distinct fake news users: ", len(distinct_fake_news_users))
    print("Distinct real and fake news users: ", len(distinct_real_fake_news_users))

if __name__ == '__main__':
    # classify_and_write() # uncomment and run to re-create separate files
    print_distinct_users()
