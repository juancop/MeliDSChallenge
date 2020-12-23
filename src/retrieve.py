# A class that retrieves the information of all products listed on MercadoLibre in a given country.
# Developed by Juan Eduardo Coba Puerto - Based on the documentation available at https://developers.mercadolibre.com.co
import requests
import pandas as pd
from collections import defaultdict

class CountryNotFound(Exception):
    pass


class productsdf:
    """
    It's a class that allows the user to donwload the information of all the listed
    items at Mercado Libre's Marketplace.
    
    """

    def __init__(self, site_name):
        """
        Params:
        --------
            site_id (str):
                A site name from which list MELI's products (https://api.mercadolibre.com/sites#json)

        """
        
        self.site_name = site_name.capitalize()
        self.site_id = self.__retrieve_site_id(self.site_name)
        self.available_categories = self.__retrieve_categories_ids()

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
        response = requests.get(url = sites_url)
        sites_list = response.json()
        site_dictionary = next((site for site in sites_list if site["name"] == site_name), None)
        if site_dictionary is None:
            raise CountryNotFound(f'The country {site_name} is not available. See available countries
             at https://api.mercadolibre.com/sites') # exception
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
        response = requests.get(url = sites_url)
        categories_list = response.json()
        categories_dictionary = {categories_list[i]['id']: categories_list[i]['name'] 
                                                                        for i in range(len(categories_list))}
        return categories_dictionary

    def list_marketplace_products(self, site_id, category_id, offset):
        page_url = f'https://api.mercadolibre.com/sites/{site_id}/search?category={category_id}&offset={offset}'
        product_request = requests.get(url = page_url).json()
        #total_products = product_request['paging']['total'] Maximum 1000 without access key
        product_json = product_request['results']
        product_df = self.single_attribute_keys(product_json)

    def iterate_through_category(self, sited_id, category_id):
        """
        
        """

    def single_attribute_keys(self, product_json):
        """
        This function combines the information retrieved by product json. Selects specific attributes
        that are easy to extract.

        Params
        --------
            product_json (dict):
                A dictionary containing the response from the API

        Returns
        --------
            result_df (pd.DataFrame)
                A pandas DataFrame with the information of each
        """
        single_attribute_keys = ['id', 'title', 'price', 'available_quantity', 'sold_quantity', 
                                 'buying_mode', 'listing_type_id', 'accepts_mercadopago',
                                 'original_price']

        merge_dictionary = defaultdict(list)

        for dictionary in product_json: # Combines the values of each key into a list.
            for key, value in dictionary.items():
                merge_dictionary[key].append(value)

        selected_features = {k:v for (k,v) in merge_dictionary.items() if k in single_attribute_keys}
        result_df = pd.DataFrame.from_dict(aaa)
        return result_df