from companies_house_api import CH 
import time
import pandas as pd
import requests
import os
import random
import string
import sqlite3

conn = sqlite3.connect('ch_db') 


KEY = os.getenv('KEY')


def make_dataset():
    ch = CH(KEY)
    sic = ch.get_sic_spreadsheet()
    df_dataset = pd.DataFrame()
    all_codes = len(sic.Code)
    print(sic.Code)
    print(f"getting data for {all_codes} sic codes")
    for sic_code in sic.Code.tolist():
        print(f"finding data for {sic_code}")
        df_to_add = ch.bare_download(sic_code)
        df_dataset = pd.concat([df_dataset,df_to_add])
        
    df_dataset_cleaned = df_dataset.drop_duplicates()
    print(f"got {len(df_dataset_cleaned)} company records")
    df_dataset_cleaned.to_sql(con=conn,name='ch_data',if_exists='replace')
    df_dataset_cleaned.to_csv('ch_dataset.csv')




make_dataset()
