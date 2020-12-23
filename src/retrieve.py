# A class that retrieves the information of all products listed on MercadoLibre in a given country.
import requests

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

