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

    Params
    -------
        site_name (string):
            The country of interest
        
        token (string):
            MELI's API Token to make
    
    """

    def __init__(self, site_name, token, folder = 'data', keep_individual_memory = False):
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
        self.keep_individual_memory = keep_individual_memory

    def create_dataset(self, export_file = False, file_name = 'results.csv', products_per_category = 5000, export_individual = True, check_existence = True):
        """
        Creates a DataSet listing all available products in Mercado Libre's Marketplace
        """

        category_dataframes = [self.iterate_through_category(self.site_id, category_id, export_individual, check_existence, products_per_category) 
                                        for category_id in progressbar(self.available_categories.keys())]
        #category_dataframes = []
        #for category_id in tqdm(self.available_categories.keys()):
        #    print(category_id)
        #    category_df = self.iterate_through_category(self.site_id, category_id) 
        #    category_dataframes.append(category_df)
        if self.keep_individual_memory:
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
            nested_df = self.multiple_attribute_keys_df(product_json)

            product_df = product_df.merge(nested_df, on = 'id')
            return product_df
        except Exception as e:
            print(e)

    def iterate_through_category(self, site_id, category_id, export_individual = True, check_existence = True, products_per_category = 5000):
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
        max_value = self.find_maximum_value(category_id, products_per_category)
        if check_existence:
            try:
                complete_category_df = pd.read_csv(path, sep = ";")
            except:
                time.sleep(0.05)
                page_df_by_offset = [self.list_marketplace_products(self.site_id, category_id, offset) 
                                            for offset in range(0, max_value, 50)]

                #page_df_by_offset = []
                #for offset in range(0, 101, 50):
                #    tmp_df = self.list_marketplace_products(self.site_id, category_id, offset)
                #    page_df_by_offset.append(tmp_df)

                complete_category_df = pd.concat(page_df_by_offset, axis = 0, ignore_index=True)
                complete_category_df['category_name'] = self.available_categories[category_id]
                if export_individual:
                    complete_category_df.to_csv(path, sep = ';', index = False)
        if self.keep_individual_memory:
            return complete_category_df

    def find_maximum_value(self, category_id, products_per_category):
        """
        Finds the maximum value of products available for retrieving. 
        """
        url = f'https://api.mercadolibre.com/categories/{category_id}'
        r = requests.get(url = url, headers = self.authorization_token)
        category_info = r.json()
        total_items_in_this_category = category_info['total_items_in_this_category']
        maximum_allowed = min(products_per_category, total_items_in_this_category)
        return maximum_allowed




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
        
        seller_attributes = self.iterate_and_combine(product_json, self.extract_seller_attributes)
        product_info = self.iterate_and_combine(product_json, self.extract_nested_product_info)    
        update_info = self.iterate_and_combine(product_json, self.date_information)
        question_info = self.iterate_and_combine(product_json, self.retrieve_date_and_questions)

        list_of_features = [product_info, update_info, question_info]
        for information in list_of_features:
            seller_attributes.update(information)

        result_df = pd.DataFrame.from_dict(seller_attributes)
        return result_df

    def iterate_and_combine(self, product_json, function):
        """
        Iterates through the JSON and retrieves the fields based on the function of interest.

        Params
        --------
            product_json (dictionary):
                A dictionary containing the 'results' response from MELI's API

            function (function):
                A function that performs extraction of fields.

        Returns
        --------
            merge_dictionary (dictionary):
                A dictionary containing a list of all results from the function of interest.

        """
        n_elements = len(product_json)
        dictionary_list = [function(product_json, idx) for idx in range(n_elements)]

        merge_dictionary = defaultdict(list)

        for dictionary in dictionary_list: # Combines the values of each key into a list.
            for key, value in dictionary.items():
                merge_dictionary[key].append(value)
        
        return merge_dictionary
    
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

    def extract_seller_attributes(self, product_json, idx):
        """
        Extract information about the reputation of the seller in the Marketplace
        """
        seller_info = product_json[idx]['seller']
        seller_registration = seller_info.get('registration_date')
        seller_level_id = seller_info.get('seller_reputation', {}).get('level_id')
        seller_powerseller = seller_info.get('seller_reputation', {}).get('power_seller_status')
        positive_rating = seller_info.get('seller_reputation', {}).get('transactions', {}).get('ratings', {}).get('positive') # Computar un NPS
        negative_rating = seller_info.get('seller_reputation', {}).get('transactions', {}).get('ratings', {}).get('negative')
        neutral_rating = seller_info.get('seller_reputation', {}).get('transactions', {}).get('ratings', {}).get('neutral')
        
        seller_attributes_dict = {
            'seller_level_id': seller_level_id,
            'seller_powerseller': seller_powerseller,
            'positive_rating': positive_rating,
            'negative_rating': negative_rating,
            'neutral_rating': neutral_rating
        }
        
        return seller_attributes_dict

    def extract_nested_product_info(self, product_json, idx):
        """
        Extracts additional information of the product, such as shipping and tags.
        """
        product_info = product_json[idx]
        product_id = product_info['id']
        free_shipping = product_info['shipping']['free_shipping']
        store_pickup = product_info['shipping']['store_pick_up']
        number_of_tags = len(product_info['tags'])
        is_official_store = (product_info['official_store_id'] is not None)
        
        product_information_dict = {
            'id' : product_id,
            'free_shipping' : free_shipping, 
            'store_pickup' : store_pickup,
            'number_of_tags' : number_of_tags,
            'is_official_store': is_official_store        
        }
        
        return product_information_dict
        

    def date_information(self, product_json, idx):
        """
        Extract the last time of product updating based on thumbnail information
        """
        thumbnail_info = product_json[idx].get('thumbnail')
        if thumbnail_info is not None:
            thumbnail_date = thumbnail_info.split('_')[-1]
            month_update = thumbnail_date[:2]
            year_update = thumbnail_date[2:6]
        else:
            month_update, year_update = None, None
        
        update_info = {
            'month_update' : month_update,
            'year_update' : year_update
        }
        
        return update_info 

    def retrieve_date_and_questions(self, product_json, idx):
        time.sleep(0.5)
        product_id = product_json[idx]['id']
        url = f'https://api.mercadolibre.com/questions/search?item={product_id}&sort_fields=date_created&limit=1'
        r = requests.get(url = url, headers = self.authorization_token)
        question_json = r.json()
        total = question_json.get('total')
        questions = question_json.get('questions', [])
        if questions:
            fecha_primera = questions[0]['date_created'].split('-')
            year_created, month_created = fecha_primera[0], fecha_primera[1]
        else:
            year_created, month_created = None, None
        
        question_date = {
            'year_created' : year_created,
            'month_created' : month_created,
            'total_questions': total
        }
        return question_date

