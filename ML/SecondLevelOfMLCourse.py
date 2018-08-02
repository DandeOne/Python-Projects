import pandas as pd
import sklearn

main_file_path = 'train.csv'
data = pd.read_csv(main_file_path)

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

data_target = data.SalePrice
predictors = data.drop(['SalePrice'], axis = 1)

numeric_predictors = predictors.select_dtypes(exclude=['object'])

X_train, X_test, y_train, y_test = train_test_split(numeric_predictors, 
                                                    data_target,
                                                    train_size=0.7, 
                                                    test_size=0.3, 
                                                    random_state=0)

def score_dataset(X_train, X_test, y_train, y_test):
    model = RandomForestRegressor()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return mean_absolute_error(y_test, preds)

cols_with_missing = [col for col in X_train.columns 
                                 if X_train[col].isnull().any()]
reduced_X_train = X_train.drop(cols_with_missing, axis=1)
reduced_X_test  = X_test.drop(cols_with_missing, axis=1)
print("Mean Absolute Error from dropping columns with Missing Values:")
print(score_dataset(reduced_X_train, reduced_X_test, y_train, y_test))

from sklearn.preprocessing.imputation import Imputer

my_imputer = Imputer()
imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
imputed_X_train.columns = numeric_predictors.columns
imputed_X_test = my_imputer.transform(X_test)
print("Mean Absolute Error from Imputation:")
print(score_dataset(imputed_X_train, imputed_X_test, y_train, y_test))

imputed_X_train_plus = X_train.copy()
imputed_X_test_plus = X_test.copy()

cols_with_missing = (col for col in X_train.columns 
                                 if X_train[col].isnull().any())
for col in cols_with_missing:
    imputed_X_train_plus[col + '_was_missing'] = imputed_X_train_plus[col].isnull()
    imputed_X_test_plus[col + '_was_missing'] = imputed_X_test_plus[col].isnull()
temp_df = imputed_X_test_plus 
# Imputation
my_imputer = Imputer()
imputed_X_train_plus = pd.DataFrame(my_imputer.fit_transform(imputed_X_train_plus))
imputed_X_test_plus.columns = temp_df.columns
imputed_X_test_plus = my_imputer.transform(imputed_X_test_plus)

print("Mean Absolute Error from Imputation while Track What Was Imputed:")
print(score_dataset(imputed_X_train_plus, imputed_X_test_plus, y_train, y_test))