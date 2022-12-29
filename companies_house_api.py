import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from collections import defaultdict 
import os

API_KEY = os.getenv("KEY")
print(API_KEY)

class CH:
    def __init__(self):
        self.auth = HTTPBasicAuth(username=API_KEY,password="")
        self.headers = headers = {
                       'Accept': 'application/json',
                              'Authorization' : API_KEY
                              }
        self.url = "https://api.company-information.service.gov.uk/advanced-search/companies"
    def search_name(self,name):
        params = {'company_name_includes':name}
        response = requests.get(url=self.url,params=params,auth=self.auth)
        


