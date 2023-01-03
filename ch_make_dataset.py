from companies_house_api import CH 

def make_dataset():
    ch = CH()
    search_df = ch.search(name_inc="ppx")
    print(search_df)
make_dataset()
