from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV
from xgboost import XGBClassifier

def GridSearchXGBClassifier(num_class):
    XGB = XGBClassifier(objective='multi:softmax', num_class = num_class, n_jobs=3)
    xgb_params  = [
        {    
        "n_estimators": range(200, 800, 100),
        }
    ]

    cv = StratifiedShuffleSplit(n_splits=3, test_size=0.3, random_state=42)

    XGB_to_fit = GridSearchCV(XGB, xgb_params, scoring='f1_macro', cv=cv, verbose=3)
    return XGB_to_fit



    Model_1.fit(X_train, y_train)