import re
import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
from collections import defaultdict 
import os
import json
import pandas as pd



class CH:

    def __init__(self,api_key):
        self.search_url = "https://api.company-information.service.gov.uk/advanced-search/companies"
        self.company_info_url = "https://api.company-information.service.gov.uk/company/"
        self.tb = pd.read_html('https://developer-specs.company-information.service.gov.uk/companies-house-public-data-api/resources/companyprofile?v=latest')[0]
        self.tb_no_obj = self.tb[self.tb.Type != 'object'].Name.tolist()
        self.columns = list(map(lambda x: re.sub("\.","_",x),self.tb_no_obj))
        self.api_key = api_key
        self.auth = HTTPBasicAuth(username=api_key,password="")
        

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
        print(response)
        company_numbers =  list(map(lambda x: x['company_number'],response.json()['items']))
        df = self.make_dataframe_from_numbers(company_numbers)
        return df

    def get_company_data(self,company_number: str) -> pd.DataFrame:
        """ helper method to get dataframe for a company """
        response = requests.get(url=self.company_info_url+company_number,auth=self.auth)
        ch_data = defaultdict(str,response.json())
        accounts = defaultdict(str,ch_data['accounts'])
        links = defaultdict(str,ch_data['links'])
        address = defaultdict(str,ch_data['registered_office_address'])
        annual_return = defaultdict(str,ch_data['annual_return'])
        branch_company_details = defaultdict(str,ch_data['branch_company_details']) 
        confirmation_statement = defaultdict(str,ch_data['confirmation_statement']) 
        of_addr = defaultdict(str,ch_data['registered_office_address']) 
        foreign_company_details = defaultdict(str,ch_data['foreign_company_details']) 
        f_accounts = defaultdict(str,foreign_company_details['accounts']) 
        f_acc_req = defaultdict(str,foreign_company_details['accounting_requirement'])
        prev_company = defaultdict(str,ch_data['previous_company']) 
        srv_addr = defaultdict(str,ch_data['service_address']) 
        links = defaultdict(str,ch_data['links']) 
        df_ch = pd.DataFrame()


        df_ch['company_name'] = [ch_data['company_name']]
        df_ch['company_number'] = [ch_data['company_number']]
        df_ch['company_status'] =  [ch_data['company_status']]
        df_ch['company_status_detail'] = [ch_data['company_status_detail']]
        df_ch['accounts_accounting_reference_date_day'] = [accounts['accounting_reference_date']['day']]
        df_ch['accounts_accounting_reference_date_month'] = [accounts['accounting_reference_date']['month']]
        df_ch['accounts_last_accounts_made_up_to'] = [accounts['last_accounts_made_up_to']]
        df_ch['accounts_next_due'] = [accounts['next_due']]
        df_ch['accounts_next_made_up_to'] = [accounts['next_made_up_to']]
        df_ch['accounts_overdue'] = [accounts['accounts_overdue']]
        df_ch['annual_return_last_made_up_to'] = [annual_return['last_made_up_to']]
        df_ch['annual_return_next_due'] = [annual_return['next_due']]
        df_ch['annual_return_next_made_up_to'] = [annual_return['next_made_up_to']]
        df_ch['annual_return_overdue'] = [annual_return['overdue']]
        df_ch['branch_company_details_business_activity'] = [branch_company_details['business_activity']]
        df_ch['branch_company_details_parent_company_name'] = [branch_company_details['parent_company_name']]
        df_ch['branch_company_details_parent_company_number'] = [branch_company_details['parent_company_number']]
        df_ch['can_file'] = [ch_data['can_file']]
        df_ch['confirmation_statement_last_made_up_to'] = [confirmation_statement['last_made_up_to']]
        df_ch['confirmation_statement_next_due'] =[confirmation_statement['next_due']]
        df_ch['confirmation_statement_next_made_up_to'] =[confirmation_statement['next_made_up_to']]
        df_ch['confirmation_statement_overdue'] = [confirmation_statement['overdue']]
        df_ch['date_of_cessation'] = [ch_data['date_of_cessation']]
        df_ch['date_of_creation'] = [ch_data['date_of_creation']]
        df_ch['etag'] = [ch_data['etag']]
        df_ch['foreign_company_details_accounting_requirement_foreign_account_type'] = [f_acc_req['foreign_account_type']]
        df_ch['foreign_company_details_accounting_requirement_terms_of_account_publication'] = [f_acc_req['terms_of_account_publication']]
        df_ch['foreign_company_details_accounts_account_period_from:_day'] = [f_accounts['account_period_from']]
        df_ch['foreign_company_details_accounts_account_period_from:_month'] = [f_accounts['account_period_from']]
        df_ch['foreign_company_details_accounts_account_period_to_day'] = [f_accounts['account_period_to']]
        df_ch['foreign_company_details_accounts_account_period_to_month'] = [f_accounts['account_period_to']]
        df_ch['foreign_company_details_accounts_must_file_within_months'] = [f_accounts['must_file_within']]
        df_ch['foreign_company_details_business_activity'] = [foreign_company_details['business_activity']]
        df_ch['foreign_company_details_company_type'] = [foreign_company_details['company_type']]
        df_ch['foreign_company_details_governed_by'] = [foreign_company_details['governed_by']]
        df_ch['foreign_company_details_is_a_credit_finance_institution'] = [foreign_company_details['is_a_credit_finance_institution']]
        df_ch['foreign_company_details_originating_registry_country'] = [foreign_company_details['originating_registry_country']]
        df_ch['foreign_company_details_originating_registry_name'] = [foreign_company_details['originating_registry_name']]
        df_ch['foreign_company_details_registration_number'] = [foreign_company_details['registration_number']]
        df_ch['has_been_liquidated'] = [ch_data['has_been_liquidated']]
        df_ch['has_charges'] = [ch_data['has_charges']]
        df_ch['has_insolvency_history'] = [ch_data['has_insolvency_history']]
        df_ch['is_community_interest_company'] = [ch_data['is_community_interest_company']]
        df_ch['jurisdiction'] = [ch_data['jurisdiction']]
        df_ch['last_full_members_list_date'] = [ch_data['last_full_members_list_date']]
        df_ch['links_persons_with_significant_control'] = [links['persons_with_significant_control']]
        df_ch['links_persons_with_significant_control_statements'] = [links['persons_with_significant_control_statement']]
        df_ch['links_registers'] = [links['registers']]
        df_ch['links_self'] = [links['self']]
        df_ch['previous_company_names'] = [ch_data['previous_company_names']]
        df_ch['previous_company_names_ceased_on'] = [prev_company['ceased_on']]
        df_ch['previous_company_names_effective_from'] = [prev_company['effective_from']]
        df_ch['previous_company_names_name'] = [prev_company['name']]
        df_ch['registered_office_address_address_line_1'] = [of_addr['address_line_1']]
        df_ch['registered_office_address_address_line_2'] = [of_addr['address_line_2']]
        df_ch['registered_office_address_care_of'] = [of_addr['care_of']]
        df_ch['registered_office_address_country'] =  [of_addr['country']]
        df_ch['registered_office_address_locality'] = [of_addr['locality']] 
        df_ch['registered_office_address_po_box'] = [of_addr['po_box']]
        df_ch['registered_office_address_postal_code'] = [of_addr['postal_code']]
        df_ch['registered_office_address_premises'] = [of_addr['premises']]
        df_ch['registered_office_address_region'] = [of_addr['region']]
        df_ch['registered_office_is_in_dispute'] = [of_addr['is_in_dispute']]
        df_ch['service_address_address_line_1'] = [srv_addr['address_line_1']]
        df_ch['service_address_address_line_2'] = [srv_addr['address_line_2']]
        df_ch['service_address_care_of'] = [srv_addr['care_of']]
        df_ch['service_address_country'] = [srv_addr['country']]
        df_ch['service_address_locality'] = [srv_addr['locality']]
        df_ch['service_address_po_box'] = [srv_addr['po_box']]
        df_ch['service_address_postal_code'] = [srv_addr['postal_code']]
        df_ch['service_address_region'] = [srv_addr['region']]
        df_ch['sic_codes'] = [ch_data['sic_codes']]
        df_ch['super_secure_managing_officer_count'] = [ch_data['super_secure_managing_officer_count']]
        df_ch['type'] = [ch_data['type']]
        df_ch['undeliverable_registered_office_address'] = [ch_data['undeliverable_registered_office_address']]

        return df_ch

    def make_dataframe_from_numbers(self,company_numbers_list: list) -> pd.DataFrame:
        """ gets more detailed information from each company from their companies house number and returns it as a dataframe  """
        dfs = list(map(self.get_company_data,company_numbers_list))
        master_df = pd.concat(dfs,ignore_index=True)
        return master_df
    def get_people_from_company_list(self,company_list: list) -> pd.DataFrame:
        return None
        
    def get_revenue_from_company_list(self,company_list: list) -> pd.DataFrame:
        return None

    def get_employ_data_from_company_list(self,company_list: list) -> pd.DataFrame:
        return None




        


