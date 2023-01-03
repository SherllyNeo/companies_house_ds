from companies_house_api import CH 
import os

KEY = os.getenv('KEY')

def make_dataset():
    ch = CH(api_key=KEY)
    search_df = ch.search(name_inc="ppx")
    print(search_df)
make_dataset()
