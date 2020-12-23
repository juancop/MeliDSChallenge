# A class that retrieves the information of all products listed on MercadoLibre in a given country.
# Developed by Juan Eduardo Coba Puerto - Based on the documentation available at https://developers.mercadolibre.com.co

import os
import time
import requests
import pandas as pd
from tqdm import tqdm 
from progressbar import progressbar
from collections import defaultdict

class CountryNotFound(Exception):
    pass

class meliRetriever:
    """
    It's a class that allows the user to donwload the information of all the listed
    items at Mercado Libre's Marketplace.
    
    """

    def __init__(self, site_name, token, folder = 'data'):
        """
        Params:
        --------
            site_id (str):
                A site name from which list MELI's products (https://api.mercadolibre.com/sites#json)

        """
        
        self.site_name = site_name.capitalize()
        self.authorization_token =  {
                            'Authorization': f'Bearer {token}' 
                        }
        self.site_id = self.__retrieve_site_id(self.site_name)
        self.available_categories = self.__retrieve_categories_ids()
        self.folder = folder
        

    def create_dataset(self, export_file = True, file_name = 'results.csv', export_individual = True, check_existence = True):
        """
        Creates a DataSet listing all available products in Mercado Libre's Marketplace
        """

        category_dataframes = [self.iterate_through_category(self.site_id, category_id, export_individual, check_existence) 
                                        for category_id in progressbar(self.available_categories.keys())]
        #category_dataframes = []
        #for category_id in tqdm(self.available_categories.keys()):
        #    print(category_id)
        #    category_df = self.iterate_through_category(self.site_id, category_id) 
        #    category_dataframes.append(category_df)

        complete_site_df = pd.concat(category_dataframes, axis = 0, ignore_index=True)
        if export_file:
            complete_site_df.to_csv(file_name, sep = ';', index = False)
        return complete_site_df

    def __retrieve_site_id(self, site_name):
        """
        Retrieves the site_id of the selected country.

        Params:
        ---------
            site_name (string):
                The name of the country of interest
            
        Returns
        ---------
            site_id (string):
                The site ID based on MELI's definition. 
        """
        sites_url = "https://api.mercadolibre.com/sites"
        response = requests.get(url = sites_url, headers = self.authorization_token)
        sites_list = response.json()
        site_dictionary = next((site for site in sites_list if site["name"] == site_name), None)
        if site_dictionary is None:
            raise CountryNotFound(f'The country {site_name} is not available. See available countries at https://api.mercadolibre.com/sites') # exception
        else:
            return site_dictionary['id']

    def __retrieve_categories_ids(self):
        """
        Retrieves all categories and their IDs available at a certain country.

        Returns
        ---------
            categories_dictionary (dict):
                A dictionary containing {category_id: category_name}
        """
        categories_url = f'https://api.mercadolibre.com/sites/{self.site_id}/categories'
        response = requests.get(url = categories_url, headers = self.authorization_token)
        categories_list = response.json()
        categories_dictionary = {categories_list[i]['id']: categories_list[i]['name'] 
                                                                        for i in range(len(categories_list))}
        return categories_dictionary

    def list_marketplace_products(self, site_id, category_id, offset):
        """
        Retrieves a fraction of the listed products.

        Params
        --------
            site_id (string): 
                The ID of the country of interest
            
            category_id (string):
                The ID of the category of interest

            offset (integer):
                Starting point of the request.

        Returns
        ---------
            product_df (pandas.DataFrame):
                A DataFrame containing all the single-valued information for each product
        """
        page_url = f'https://api.mercadolibre.com/sites/{site_id}/search?category={category_id}&offset={offset}'
        product_request = requests.get(url = page_url, headers = self.authorization_token).json()
        #total_products = product_request['paging']['total'] Maximum 1000 without access key
        try:
            product_json = product_request['results']
            product_df = self.single_attribute_keys_df(product_json)
            return product_df
        except:
            pass

    def iterate_through_category(self, site_id, category_id, export_individual = True, check_existence = True):
        """
        Lists all the products in a given category.

        Params
        --------
            site_id (string): 
                The ID of the country of interest
            
            category_id (string):
                The ID of the category of interest
        
        Returns
        --------
            complete_category_df (pandas.DataFrame):
                A DataFrame containing all the retrieved information for a given category
        """
        path = os.path.join(self.folder, f'{category_id}.csv')

        if check_existence:
            try:
                complete_category_df = pd.read_csv(path, sep = ";")
            except:
                time.sleep(0.05)
                page_df_by_offset = [self.list_marketplace_products(self.site_id, category_id, offset) 
                                            for offset in range(0, 1051, 50)]

                complete_category_df = pd.concat(page_df_by_offset, axis = 0, ignore_index=True)
                complete_category_df['category_name'] = self.available_categories[category_id]
                if export_individual:
                    complete_category_df.to_csv(path, sep = ';', index = False)
        return complete_category_df

    def multiple_attribute_keys_df(self, product_json):
        """
        This function extract the nested attributes. 

        Params
        --------
            product_json (dict):
                A dictionary containing the response from the API

        Returns
        --------
            result_df (pandas.DataFrame)
                A pandas DataFrame with the information of each product
        """




    def single_attribute_keys_df(self, product_json):
        """
        This function combines the information retrieved by product json. Selects specific attributes
        that are easy to extract.

        Params
        --------
            product_json (dict):
                A dictionary containing the response from the API

        Returns
        --------
            result_df (pandas.DataFrame)
                A pandas DataFrame with the information of each product
        """
        single_attribute_keys = ['id', 'category_id', 'title', 'price', 'available_quantity', 'sold_quantity', 
                                 'buying_mode', 'listing_type_id', 'accepts_mercadopago',
                                 'original_price', 'condition']

        merge_dictionary = defaultdict(list)

        for dictionary in product_json: # Combines the values of each key into a list.
            for key, value in dictionary.items():
                merge_dictionary[key].append(value)

        selected_features = {k:v for (k,v) in merge_dictionary.items() if k in single_attribute_keys}
        result_df = pd.DataFrame.from_dict(selected_features)
        return result_df


# Sample function for retrieving creation date
def retrieve_date_and_questions(token):
    time.sleep(0.05)
    url = 'https://api.mercadolibre.com/questions/search?item=MLA869879846&sort_fields=date_created&limit=1'
    header = {
        'Authorization': f'Bearer {token}' 
    }
    r = requests.get(url = url, headers = header)
    question_json = r.json()
    print(question_json)
    total = question_json['total']
    questions = question_json['questions']
    if questions:
        fecha_primera = questions[0]['date_created'].split('-')
        year_created, month_created = fecha_primera[0], fecha_primera[1]
    else:
        year_created, month_created = None, None
    
    return total, year_created, month_created