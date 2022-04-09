import config

import pandas as pd
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.chrome.webdriver import WebDriver
import warnings
from sqlalchemy import create_engine
import os
from datetime import date

warnings.filterwarnings('ignore')

def get_table(soup):
    for t in soup.select('table'):
        header = t.select('thead tr th')
        if len(header) > 2:
            if (header[0].get_text().strip() == 'Symbol'
                and header[2].get_text().strip().startswith('% Holding')):
                return t
    raise Exception('could not find symbol list table')
    
# Scrapes ETF holdings from barchart.com
def get_etf_holdings(etf_symbol,d):
    '''
    etf_symbol: str
    
    return: pd.DataFrame

    '''
    dfdata = []
    for etfs in etf_symbol:

        url = 'https://www.barchart.com/stocks/quotes/{}/constituents?page=all'.format(
            etfs)

        # Loads the ETF constituents page and reads the holdings table
        browser = WebDriver('scripts/chromedriver.exe') # webdriver.PhantomJS()
        browser.get(url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html')
        table = get_table(soup)

        # Reads the holdings table line by line and appends each asset to a
        # dictionary along with the holdings percentage
        asset_dict = {}
        for row in table.select('tr')[1:-1]:
            try:
                cells = row.select('td')
            
                symbol = cells[0].get_text().strip()

                name = cells[1].text.strip()
                celltext = cells[2].get_text().strip()
                percent = celltext.rstrip('%')
                shares = cells[3].text.strip().replace(',', '')
                if symbol != "" and percent != 0.0:
                    asset_dict[symbol] = {
                        'name': name,
                        'percent': percent,
                        'shares': shares,
                    }
                output = pd.DataFrame(asset_dict).T.reset_index().rename(columns={'index':'symbol'})
                output['fund'] = etfs
                output.to_csv(f'data/{d}/{etfs}.csv',index=False)
                dfdata.append(output)
            except BaseException as ex:
                print(ex)
        browser.quit()
    
    return pd.concat(dfdata)


if __name__=='__main__':
    d = (str(date.today().year) + '-' +
     str(date.today().month).zfill(2) + '-' +
     str(date.today().day).zfill(2))
    
    if not os.path.exists(f'data'):
        os.mkdir(f'data')
    if not os.path.exists('data/' + d):
        os.mkdir('data/' + d)

    engine = create_engine(f'postgresql://postgres:{config.DB_PASS}@{config.DB_HOST}:5432/{config.DB_NAME}')

    connection = engine.connect()

    sql = "SELECT * FROM stock WHERE is_etf = TRUE"

    #stocks = pd.read_sql(sql,connection)['symbol'].to_list()
    df = get_etf_holdings(['SPYD'],d)
    print(tuple(df['fund'].value_counts().to_frame().reset_index()['index']))
    

