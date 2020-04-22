import sys
import csv
from main import ch_download, get_filing_history, get_latest_conf_stmt, get_company_name, create_folder

def get_stat_pdfs(csv_file, filing_history=True, officers=True, charges=True, conf_stmt=True):
    with open (csv_file) as file:
        csv_file = csv.reader(file, delimiter=',')
        for row in csv_file:
            company_number = row[0]
            ch_download(company_number, filing_history=filing_history, officers=officers, charges=charges)
            if conf_stmt:
                get_latest_conf_stmt(company_number)

if __name__ == '__main__':
    # Map command line arguments to function arguments.
    get_stat_pdfs(*sys.argv[1:])