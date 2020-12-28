import xgboost as xgb
from xgboost import XGBClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import KFold
from scipy import stats

def define_xgb_for_cv(num_class, scoring = 'f1_macro'):
    """
    XGB Initial parameter distribution
    
    """
    param_dist = {'n_estimators': stats.randint(150, 1000),
              'learning_rate': stats.uniform(0.01, 0.07),
              'subsample': stats.uniform(0.3, 0.7),
              'max_depth': [3, 4, 5, 6, 7, 8, 9],
              'colsample_bytree': stats.uniform(0.5, 0.45),
              'min_child_weight': [1, 2, 3]
             }

    kfold_3 = KFold(n_splits = 3, shuffle = True, random_state=42)


    model = XGBClassifier(n_estimators=100,
                         reg_lambda=1,
                         gamma=0,
                         max_depth=3,
                         objective = 'multi:softmax',
                         n_jobs = -1,
                         num_class = num_class)

    model_cv = RandomizedSearchCV(model, 
                             param_distributions = param_dist,
                             cv = kfold_3,  
                             n_iter = 5, 
                             scoring = scoring, 
                             error_score = 0, 
                             verbose = 1, 
                             n_jobs = -1)
    
    return model_cv

## XGB_model = define_xgb_for_cv(num_class, 'f1_macro')
## XGB_model.fit(X_train, y_train)
## XGB_model.best_params_
