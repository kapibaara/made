import numpy
import pandas
from catboost import CatBoostClassifier
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import KFold
from xgboost import XGBClassifier
import seaborn as sns
import matplotlib.pyplot as plt

X = pandas.read_csv('train_1.csv')
y = pandas.read_csv('./train-target.csv').to_numpy().flatten()

sns.pairplot(X)
sns.heatmap(X.corr(), annot=True)
plt.show()

drop_columns = [9, 15, 16, 17, 22, 26]

X = X.drop(X.columns[drop_columns], axis=1).to_numpy()

# # Сокращение признаков
pca = PCA(n_components=15)
pca.fit(X)
X = pca.fit_transform(X)
#
# Обучение
kf = KFold(n_splits=5, shuffle=True, random_state=1)
rfc = RandomForestClassifier(random_state=42, n_estimators=35)
lr = LogisticRegression(random_state=241, class_weight='balanced')
cat = CatBoostClassifier(random_state=241)
xg = XGBClassifier(random_state=42)

#
def fit_model(model):
    scores = []

    for train, test in kf.split(X):
        X_train, X_test = X[train], X[test]
        y_train, y_test = y[train], y[test]

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        score = roc_auc_score(y_test, predictions)
        scores.append(score)

    print(numpy.mean(scores))


fit_model(rfc)
fit_model(cat)
# fit_model(xg)
fit_model(lr)

X_test = pandas.read_csv('./test.csv')
X_test = pca.transform(X_test)

pred_test = cat.predict_proba(X_test)[:, 1]

pandas.DataFrame(pred_test).to_csv('./predictions.csv', index=False, header=False)