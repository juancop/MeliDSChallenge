# API Token Retriever for Mercado Libre API.
# This code was developed by Juan Eduardo Coba Puerto based on 
#           Python SDK Documentation: https://github.com/mercadolibre/python-sdk
# Useful: https://developers.mercadolibre.com.ar/es_ar/autenticacion-y-autorizacion/
# 
# The provided API Key will die after 6 hourse (based on the documentation)

import time
import meli
from meli.rest import ApiException
from pprint import pprint
import urllib
from getpass import getpass
# Defining the host, defaults to https://api.mercadolibre.com
# See configuration.py for a list of all supported configuration parameters.
configuration = meli.Configuration(
    host = "https://api.mercadolibre.com"
)

class getAPIkey:

    def __init__(self):
        self.retrieve_url()
        self.request_code = self.ask_code_from_user()
        self.api_key = self.APIKey()
        
    def retrieve_url(self):
        params = urllib.parse.urlencode({
                                            'response_type':'code', 
                                            'client_id':'4892726125387151', 
                                            'redirect_uri':'https://www.mercadolibre.com.co/'
                                        })
        f = urllib.request.urlopen("https://auth.mercadolibre.com.co/authorization?%s" % params)

        print(f.geturl())
    
    def ask_code_from_user(self):
        return getpass('Please write the code:')

    def APIKey(self):
        with meli.ApiClient() as api_client:
        # Create an instance of the API class
            api_instance = meli.OAuth20Api(api_client)
            grant_type = 'authorization_code' # str
            client_id = '4892726125387151' # Your client_id
            client_secret = '4892726125387151' # Your client_secret
            redirect_uri = 'https://www.mercadolibre.com.co/' # Your redirect_uri
            #refresh_token = 'refresh_token_example' # Your refresh_token

        try:
            # Request Access Token
            api_response = api_instance.get_token(grant_type=grant_type, client_id=client_id,
                             client_secret=client_secret, redirect_uri=redirect_uri, 
                             code=self.request_code, refresh_token=self.request_code)
            return api_response['access_token']
        except ApiException as e:
            print("Exception when calling OAuth20Api->get_token: %s\n" % e)

