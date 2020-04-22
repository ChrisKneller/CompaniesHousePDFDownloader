# CompaniesHousePDFDownloader
A python tool to download PDFs of various data from Companies House. Requires pdfkit and wkhtmltopdf (https://pypi.org/project/pdfkit/).

This tool will download, for each company:
- The company's latest [confirmation statement](https://beta.companieshouse.gov.uk/company/03977902/filing-history/MzI2Mjc1OTI1OWFkaXF6a2N4/document?format=pdf&download=0).
- A pdf copy of the following pages on Companies House:
  - [Filing History](https://beta.companieshouse.gov.uk/company/03977902/filing-history)
  - [Officers](https://beta.companieshouse.gov.uk/company/03977902/officers)
  - [Charges](https://beta.companieshouse.gov.uk/company/03977902/charges)

## Usage
- Install pdfkit and wkhtmltopdf. Instructions [here](https://pypi.org/project/pdfkit/) and [here](https://github.com/JazzCore/python-pdfkit/wiki/Installing-wkhtmltopdf).
- Set up an account on Companies House and get your API key [here](https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted.html).
- Store your Companies House API key in environment variables as CH_API_KEY.
- Ensure you understand [HTTP Basic Authentication](https://en.wikipedia.org/wiki/Basic_access_authentication) and the method used by the [CH API](https://developer.companieshouse.gov.uk/api/docs/index/gettingStarted/apikey_authorisation.html).
- Use [this tool](https://www.blitter.se/utils/basic-authentication-header-generator/) or a similar tool to generate your basic authentication header.
- Store your generated authentication token (the "xxx" in "Basic xxx") in environment variables as CH_ACCESS_TOKEN.
- Reboot as necessary to ensure the system picks up the new environment variables.
- Clone this repo and cd into it:
```bash
git clone https://github.com/ChrisKneller/CompaniesHousePDFDownloader.git
cd CompaniesHousePDFDownloader
```
- Save a csv file with all the companies you want to check with the company number as the first entry on each row (e.g. ```03977902,Google UK Ltd,other,data,here,doesnt,matter```). This line is included in the ```companies.csv``` file in the cloned repo.
- Run the downloader on your chosen csv file:
```bash
python csv_run.py companies.csv
```

## Contributing
Pull requests are welcome. There is a lot to do on this to make it function better (e.g. tidy up the try & except statements, handle errors better, making requests asynchronous etc.). For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://github.com/ChrisKneller/CompaniesHousePDFDownloader/blob/master/LICENSE)
