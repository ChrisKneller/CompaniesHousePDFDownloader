import pdfkit
import requests
import json
from pprint import pprint
import os
from datetime import datetime

now = datetime.now()
year = now.strftime("%Y")
month = now.strftime("%m")
day = now.strftime("%d")
today_string = f"{year}{month}{day}"

BASE_URL = "https://beta.companieshouse.gov.uk/company/"

URLS = {
    "filing_history": "{}{{}}/filing-history".format(BASE_URL),
    "officers": "{}{{}}/officers".format(BASE_URL),
    "charges": "{}{{}}/charges".format(BASE_URL)
}

BASE_API_URL = "https://api.companieshouse.gov.uk/"

API_URLS = {
    "filing_history": "{}company/{{}}/filing-history".format(BASE_API_URL),
    "document_meta": "{}document/{{}}".format(BASE_API_URL),
    "document": "{}document/{{}}/content".format(BASE_API_URL),
    "company_details": "{}company/{{}}".format(BASE_API_URL)
}

API_KEY = os.environ.get('CH_API_KEY')
ACCESS_TOKEN = os.environ.get('CH_ACCESS_TOKEN')


# TODO: make asynchronous
def ch_download(company_number, filing_history=True, officers=True, charges=True, company_name=False):
    company_number = str(company_number)

    try:
        if not company_name:
            company_name = get_company_name(company_number)
    except Exception as e:
        print(f"Company not found on Companies: {e}")
        return

    directory = create_folder(company_name)

    if filing_history:
        try:
            pdfkit.from_url(URLS['filing_history'].format(company_number),
                            os.path.join(directory, f'{today_string}-filing-history.pdf'))
        except OSError as e:
            print(f"Doesn't exist; skipped: {e}")
    if officers:
        try:
            pdfkit.from_url(URLS['officers'].format(company_number),
                            os.path.join(directory, f'{today_string}-officers.pdf'))
        except OSError as e:
            print(f"Doesn't exist; skipped: {e}")
    if charges:
        try:
            pdfkit.from_url(URLS['charges'].format(company_number),
                            os.path.join(directory, f'{today_string}-charges.pdf'))
        except OSError as e:
            print(f"Doesn't exist; skipped: {e}")

                    
def get_filing_history(company_number):
    company_number = str(company_number)
    r = requests.get(API_URLS['filing_history'].format(company_number),
                     auth=(API_KEY, ''))
    print(r)
    data = json.loads(r.text)
    return data


def get_latest_conf_stmt(company_number, company_name=False):
    try:
        if not company_name:
            company_name = get_company_name(company_number)
    except Exception as e:
        print(f"Company not found on Companies: {e}")
        return

    # get the filing history of the company
    try:
        data = get_filing_history(company_number)
        items = data['items']
        itemsIterator = iter(items)
    except Exception as e:
        print(f'Unable to get filing history: {e}')
        return
    
    # find the latest confirmation statement (and extra various data)
    try:
        conf_stmt = (x for x in itemsIterator if x['category'] == 'confirmation-statement').__next__()
        alt_meta_link = conf_stmt['links']['document_metadata']
    except Exception as e:
        print(f'Unable to find confirmation statement: {e}')
        return

    # get metadata of document and extract file link for document fetch request
    r = requests.get(alt_meta_link,auth=(API_KEY, ''))
    metadata = json.loads(r.text)
    file_link = metadata['links']['document']

    # define headers for document fetch request
    headers = {
        "Accept": "application/pdf",
        "Authorization": "Basic " + ACCESS_TOKEN
    }

    # fetch document
    with requests.get(file_link, headers=headers) as response:
        pdf_link = response.url
        r = requests.get(pdf_link)
        
        # create directory with company name if not already existing
        directory = create_folder(company_name)
        file_name = f'{today_string}-confirmation-statement.pdf'

        with open(f'{os.path.join(directory,file_name)}', 'wb') as file:
            file.write(r.content)
            return response


def get_company_name(company_number):
    r = requests.get(API_URLS['company_details'].format(company_number),
                     auth=(API_KEY, ''))
    data = json.loads(r.text)
    company_name = data['company_name']
    return company_name


def create_folder(folder_name):
    try:
        # Create target Directory
        os.mkdir(folder_name)
        print(f"Directory {folder_name} created ") 
    except FileExistsError:
        print(f"Directory {folder_name} already exists")
    return folder_name