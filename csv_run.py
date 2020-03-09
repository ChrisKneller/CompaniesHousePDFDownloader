import csv
from main import ch_download, get_filing_history, get_latest_conf_stmt, get_company_name, create_folder

csv_file = 'aw_clients.csv'

def get_stat_pdfs(csv_file):
    with open (csv_file) as file:
        csv_file = csv.reader(file, delimiter=',')
        for row in csv_file:
            company_number = row[0]
            ch_download(company_number)
            get_latest_conf_stmt(company_number)

get_stat_pdfs(csv_file)