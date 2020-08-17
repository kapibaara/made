import pandas
import numpy

train = pandas.read_csv('/Users/a.boldovskaya/Downloads/train (1).csv', usecols=range(3))
test = pandas.read_csv('/Users/a.boldovskaya/Downloads/test (1).csv')
item_features = pandas.read_csv('/Users/a.boldovskaya/Downloads/item-features (1).csv')

view_by_user = train.drop(columns=['like']).groupby('user_id')
train_with_likes = train[train['like'] == 1].drop(columns=['user_id'])

view_by_user_dict = view_by_user.apply(lambda g: list(map(lambda x: x[1], g.values)))
#

sorted_likes = train_with_likes\
    .groupby('item_id')\
    .sum()\
    .sort_values(by='like', ascending=False)


def get_mean(item_id):
    item_raw = item_features.iloc[item_id]

    return numpy.mean(item_raw)


def get_top_likes(user_id):
    user_views = numpy.unique(view_by_user_dict[user_id])

    without_viewed = numpy.setdiff1d(
        sorted_likes.index.values,
        user_views,
        True
    )

    return without_viewed[:20]


result = map(
    lambda id: [id, *get_top_likes(id)],
    test['user_id'].to_numpy()
)
df = pandas.DataFrame(
    data=result,
    columns=['user_id', *range(20)],
)

df.to_csv('./made2/predictions_2.csv', index=False)