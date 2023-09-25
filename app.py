from flask import Flask, request, render_template
import requests
import pandas as pd
import numpy as np



app = Flask(__name__)

# Create the user header to access the SEC API

headers = {'User-Agent': "email@email.com"}

# Importing the Tickers, CIK and Company Name from the SEC

companyTickers = requests.get("https://www.sec.gov/files/company_tickers.json", headers=headers)

companyData = pd.DataFrame.from_dict(companyTickers.json(), orient='index')


# Routes start from here


# Route for index.html

@app.route('/', methods = ['GET', 'POST'])
def index():
    # headers = companyData.columns
    # rows = companyData.values
    return render_template('index.html')

# Route for search.html (This opens after the search has been made)

@app.route('/search', methods = ['GET','POST'])
def search():
    if request.method == 'POST':
        searched = request.form['search']
        # start = request.form['start']
        # end = request.form['end']
    searched_query = searched
    cik = companyData.loc[companyData['ticker'] == searched_query , 'cik_str']
    cik = int(cik)
    cik = str(cik)
    cik = cik.zfill(10)
    # Getting the company facts from the SEC API

    companyFacts = requests.get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json', headers=headers)

    dates = ['CY1994', 'CY1995', 'CY1996', 'CY1997', 'CY1998', 'CY1999', 'CY2000', 'CY2001', 'CY2002', 'CY2003', 'CY2004', 'CY2005', 'CY2006', 'CY2007', 'CY2008', 'CY2009', 'CY2010', 'CY2011', 'CY2012', 'CY2013', 'CY2014', 'CY2015','CY2016', 'CY2017', 'CY2018', 'CY2019', 'CY2020', 'CY2021', 'CY2022', 'CY2023']
    
    
    # Getting revenue, Gross Profit and Net income loss of requested company
    try:
        Revenue = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['RevenueFromContractWithCustomerExcludingAssessedTax']['units']['USD'])
        Revenue = Revenue[(Revenue['form'] == '10-K') & (Revenue['frame'].isin(dates))]
        Revenue = Revenue.drop(columns=['start','end','fp','form','filed','accn','fy'])
        Revenue['frame'] = Revenue['frame'].str.replace('CY', '')
        # Revenue = Revenue[(Revenue['frame'] >= str(start)) & (Revenue['frame'] <= str(end))]
        Revenue_rows = Revenue.values
        Revenue_labels = [Revenue_rows[i][1] for i in range(len(Revenue_rows))]
        Revenue_values = [(Revenue_rows[i][0])/1000000000 for i in range(len(Revenue_rows))]
    
    except KeyError or NameError or TypeError:
        Revenue_rows = np.array(['-'] * 2)
        Revenue_labels = np.array(['-'] * 2)
        Revenue_values = np.array(['-'] * 2)
    
    try:
        GrossProfit = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['GrossProfit']['units']['USD'])
        GrossProfit = GrossProfit[(GrossProfit['form'] == '10-K') & (GrossProfit['frame'].isin(dates))]
        GrossProfit = GrossProfit.drop(columns=['start','end','fp','form','filed','accn','fy'])
        GrossProfit['frame'] = GrossProfit['frame'].str.replace('CY', '')
        # GrossProfit = GrossProfit[(GrossProfit['frame'] >= str(start)) & (GrossProfit['frame'] <= str(end))]
        GrossProfit_rows = GrossProfit.values 
        GrossProfit_labels = [GrossProfit_rows[i][1] for i in range(len(GrossProfit_rows))]
        GrossProfit_values = [(GrossProfit_rows[i][0])/1000000000 for i in range(len(GrossProfit_rows))]
            
    except KeyError or NameError or TypeError:
        GrossProfit_rows = np.array(['-'] * 2)
        GrossProfit_labels = np.array(['-'] * 2)
        GrossProfit_values = np.array(['-'] * 2)

    try:
        NetIncomeLoss = pd.DataFrame.from_dict(companyFacts.json()['facts']['us-gaap']['NetIncomeLoss']['units']['USD'])
        NetIncomeLoss = NetIncomeLoss[(NetIncomeLoss['form'] == '10-K') & (NetIncomeLoss['frame'].isin(dates))]
        NetIncomeLoss = NetIncomeLoss.drop(columns=['start','end','fp','form','filed','accn','fy'])
        NetIncomeLoss['frame'] = NetIncomeLoss['frame'].str.replace('CY', '')
        # NetIncomeLoss = NetIncomeLoss[(NetIncomeLoss['frame'] >= str(start)) & (NetIncomeLoss['frame'] <= str(end))]
        NetIncomeLoss_rows = NetIncomeLoss.values
        NetIncomeLoss_labels = [NetIncomeLoss_rows[i][1] for i in range(len(NetIncomeLoss_rows))]
        NetIncomeLoss_values = [(NetIncomeLoss_rows[i][0])/1000000000 for i in range(len(NetIncomeLoss_rows))]

    except KeyError or NameError or TypeError:
        NetIncomeLoss_rows = np.array(['-'] * 2)
        NetIncomeLoss_labels = np.array(['-'] * 2)
        NetIncomeLoss_values = np.array(['-'] * 2)
    
    

    table_headers = ['Value (in dollars)', 'Year']

    print(Revenue_rows)
    print(Revenue_labels)
    print(Revenue_values)
    print(GrossProfit_rows)
    print(GrossProfit_labels)
    print(GrossProfit_values)
    print(NetIncomeLoss_rows)
    print(NetIncomeLoss_labels)
    print(NetIncomeLoss_values)
    



    return render_template('search.html',
                                table_headers = table_headers, 
                                Revenue_rows = Revenue_rows, 
                                GrossProfit_rows = GrossProfit_rows, 
                                NetIncomeLoss_rows = NetIncomeLoss_rows, 
                                Revenue_labels = Revenue_labels,
                                GrossProfit_labels = GrossProfit_labels,
                                NetIncomeLoss_labels = NetIncomeLoss_labels,
                                Revenue_values = Revenue_values,
                                GrossProfit_values = GrossProfit_values,
                                NetIncomeLoss_values = NetIncomeLoss_values
                                )


if __name__ == '__main__':
    app.run(debug=True)