from companies_house_api import CH 

def make_dataset():
    ch = CH()
    response = ch.search(name_inc="ppx")
    data = ch.get_company_data(response[0])
    print(data)
make_dataset()