# Creación de Benchmark
import pandas as pd

class benchmark:
    
    def __init__(self, grouping = 2):
        self.grouping = grouping
        self.group_after = (3.5*(12/grouping) - 1) 
        self.lookup_model = None
        
    def create_group_by_months(self, row):
        """
        Creates a discretization of product_age by self.grouping months.
        """

        product_age = row.product_age

        if pd.isna(product_age):
            return -1
        else:
            group = (product_age-1)//self.grouping # Mod para dentro de un mismo grupo
            return group if group > self.group_after else self.group_after + 1

    def fit(self, X, y):
        """
        Fits the benchmark model based on modes. 
        
        Params
        --------
            X (pandas.DataFrame):
                A pandas DataFrame containing information of the products. 
                Must have product_age, golden_categories and is_new
                
        Returns
        --------
            Updates the self.lookup_model attribute. 
        
        """
        concat_df = pd.concat([X, y], axis = 1)
        concat_df['groupings'] = concat_df.apply(self.create_group_by_months, axis = 1)
        mode_by_group = concat_df.groupby('groupings').sold_quantity.apply(lambda x: x.mode()).reset_index()
        self.lookup_model = dict(zip(mode_by_group.groupings, mode_by_group.sold_quantity))

    
    def predict(self, X):
        """
        Predicts the sold_quantity based on the lookup table
        
        Params
        --------
            X (pandas.DataFrame):
                A pandas DataFrame containing information of the products. 
                Must have product_age, golden_categories and is_new
        
        Returns
        --------
            prediction_list (np.array):
                A numpy array with the prediction
        """
        X_copy = X.copy()
        X_copy['groupings'] = X_copy.apply(self.create_group_by_months, axis = 1)
        X_copy['prediction'] = X_copy.apply(self.lookup, axis = 1)
        prediction_list = X_copy.prediction.values
        return prediction_list
        
    
    def lookup(self, row):
        """
        Looks the prediction in the model dictionary.
        """
        
        grouping = row.groupings
        golden = row.golden_categories
        new = row.is_new
        initial_prediction = self.lookup_model[grouping]
        
        if new*golden:
            return initial_prediction
        else:
            return 0
       
        
        