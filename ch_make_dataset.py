from companies_house_api import CH 
from bs4 import BeautifulSoup
import pandas as pd
import requests
import os
from collections import defaultdict
from itertools import tee, islice, chain


KEY = os.getenv('KEY')


def make_dataset():
    ch = CH(api_key=KEY)
    df_sic = ch.get_sic_spreadsheet()
    print(df_sic)


make_dataset()
