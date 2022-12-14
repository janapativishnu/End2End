# Predicting car prices using data
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.interactive(True)
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import numpy as np
from sklearn.model_selection import RandomizedSearchCV

df = pd.read_csv('car data.csv')

# print(df.head())

# print(df.shape)

# print(df['Seller_Type'].unique())
# print(df['Transmission'].unique())
# print(df['Owner'].unique())
#
# # check missing or null values
# print(df.isnull().sum()) # none of them have null values

# print(df.describe())


final_dataset = df[['Year', 'Selling_Price', 'Present_Price', 'Kms_Driven',
       'Fuel_Type', 'Seller_Type', 'Transmission', 'Owner']]


final_dataset['Current_year'] = 2020

final_dataset['num_years'] = final_dataset['Current_year'] - final_dataset['Year']
final_dataset.drop(['Year'], axis=1, inplace=True)
final_dataset.drop(['Current_year'], axis=1, inplace=True)



print(final_dataset.columns)
# convert categorical into a numerical
final_dataset = pd.get_dummies(final_dataset, drop_first=True)

print(final_dataset.head())

final_dataset.corr()



# %matplotlib inline
sns.pairplot(final_dataset)


corrmat = final_dataset.corr()

top_corr_features = corrmat.index
plt.figure(figsize=(20,20))
g = sns.heatmap(final_dataset[top_corr_features].corr(), annot=True, cmap='RdYlGn')

# plt.show()

# dependent and independent features
X= final_dataset.iloc[:,1:]
y = final_dataset.iloc[:, 0]

print(X.head())



model = ExtraTreesRegressor()
model.fit(X,y)

print(model.feature_importances_)

feat_importances = pd.Series(model.feature_importances_, index = X.columns)
feat_importances.nlargest(5).plot(kind='barh')


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

print(X_train.shape)




rf_random = RandomForestRegressor()


 #Randomized Search CV

# Number of trees in random forest
n_estimators = [int(x) for x in np.linspace(start = 100, stop = 1200, num = 12)]
# Number of features to consider at every split
max_features = ['auto', 'sqrt']
# Maximum number of levels in tree
max_depth = [int(x) for x in np.linspace(5, 30, num = 6)]
# max_depth.append(None)
# Minimum number of samples required to split a node
min_samples_split = [2, 5, 10, 15, 100]
# Minimum number of samples required at each leaf node
min_samples_leaf = [1, 2, 5, 10]

# Create the random grid
random_grid = {'n_estimators': n_estimators,
               'max_features': max_features,
               'max_depth': max_depth,
               'min_samples_split': min_samples_split,
               'min_samples_leaf': min_samples_leaf}

print(random_grid)

# Use the random grid to search for best hyperparameters
# First create the base model to tune
rf = RandomForestRegressor()

# Random search of parameters, using 3 fold cross validation,
# search across 100 different combinations
rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid,scoring='neg_mean_squared_error', n_iter = 10, cv = 5, verbose=2, random_state=42, n_jobs = 1)

rf_random.fit(X_train,y_train)

RandomizedSearchCV(cv=5, estimator=RandomForestRegressor(), n_jobs=1,
                   param_distributions={'max_depth': [5, 10, 15, 20, 25, 30],
                                        'max_features': ['auto', 'sqrt'],
                                        'min_samples_leaf': [1, 2, 5, 10],
                                        'min_samples_split': [2, 5, 10, 15,
                                                              100],
                                        'n_estimators': [100, 200, 300, 400,
                                                         500, 600, 700, 800,
                                                         900, 1000, 1100,
                                                         1200]},
                   random_state=42, scoring='neg_mean_squared_error',
                   verbose=2)

print('best params of random forest', rf_random.best_params_)

print('best score of random forest', rf_random.best_score_)

predictions=rf_random.predict(X_test)

sns.distplot(y_test-predictions)

plt.scatter(y_test,predictions)

from sklearn import metrics

import pickle
# open a file, where you ant to store the data
file = open('random_forest_regression_model.pkl', 'wb')

# dump information to that file
pickle.dump(rf_random, file)
