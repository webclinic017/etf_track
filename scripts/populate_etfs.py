import config
import csv
import psycopg2
import psycopg2.extras
from datetime import date
import os
from urls import websites
import pandas as pd
import requests
from io import StringIO

def clean_ark(df):
    df = df.loc[~df['date'].str.contains('The principal risks',case=False)].reset_index().drop(columns='index')
    df['shares'] = df['shares'].str.replace(',','')
    df['weight (%)'] = df['weight (%)'].str.replace('%','')
    df['market value ($)'] = df['market value ($)'].str.replace('$','',regex=False).str.replace(',','',regex=False)
    df['date'] = pd.to_datetime(df['date']).dt.date

    return df


#headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
#
#urls = websites.split("\n")
#d = (str(date.today().year) + '-' +
#     str(date.today().month).zfill(2) + '-' +
#     str(date.today().day).zfill(2))
#
#if not os.path.exists(f'data'):
#    os.mkdir(f'data')
#os.mkdir('data/' + d)
#for url in urls:
#    
#    s=requests.get(url, headers= headers).text
#
#    c=pd.read_csv(StringIO(s), sep=",")
#    c  = clean_ark(c)
#    fund = c.loc[0,'fund']
#    c.to_csv(f'data/{d}/{fund}.csv',index=False)
#
connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("select * from stock where is_etf = TRUE")

etfs = cursor.fetchall()

dates = ['2022-04-04']

for current_date in dates:
    for etf in etfs:
        print(etf['symbol'])

        with open(f"data/{current_date}/{etf['symbol']}.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                ticker = row[3]

                if ticker: 
                    shares = row[5]
                    weight = row[7]

                    cursor.execute("""
                        SELECT * FROM stock WHERE symbol = %s
                    """, (ticker,))
                    stock = cursor.fetchone()
                    if stock:
                        print(f"Inserting a holding into {etf['symbol']}")
                        cursor.execute("""
                            INSERT INTO etf_holding (etf_id, holding_id, dt, shares, weight)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (etf['id'], stock['id'], current_date, shares, weight))

connection.commit()