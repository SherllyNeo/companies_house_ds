import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from collections import defaultdict 
import os
import json
import pandas as pd

API_KEY = os.getenv("KEY")


class CH:
    def __init__(self):
        self.auth = HTTPBasicAuth(username=API_KEY,password="")
        self.search_url = "https://api.company-information.service.gov.uk/advanced-search/companies"
        self.company_info_url = "https://api.company-information.service.gov.uk/company/"

    def search(self,name_inc="",name_ex="",company_status=None,company_sub_typ=None,company_typ=None,diss_from=None,diss_to=None,inc_from=None,inc_to=None,location=None,sic_codes=[],result_size="50",index_start=None) -> list:
        """ wrapped for company house api advanced search """
        params = {
        'company_name_includes':name_inc,
        'company_name_excludes':name_ex,
        'company_status':company_status,
        'company_subtype':company_sub_typ,
        'company_type':company_typ,
        'dissolved_from':diss_from,
        'dissolved_to':diss_to, 
        'incorporated_from':inc_from,	 
        'incorporated_to':inc_to,
        'location':location, 
        'sic_codes':sic_codes, 
        'size':result_size,
        'start_index':index_start,
        }
        response = requests.get(url=self.search_url,params=params,auth=self.auth)
        company_numbers =  list(map(lambda x: x['company_number'],response.json()['items']))
        return company_numbers

    def get_company_data(self,company_number: str) -> pd.DataFrame:
        """ helper method to get dataframe for a company """
        response = requests.get(url=self.company_info_url+company_number,auth=self.auth)
        return response.json()

    def make_dataframe_from_numbers(self,company_numbers_list: list) -> pd.DataFrame:
        """ gets more detailed information from each company from their companies house number and returns it as a dataframe  """
        





        


