import config
import csv
import psycopg2
import psycopg2.extras
from datetime import date
import pandas as pd



connection = psycopg2.connect(host=config.DB_HOST, database=config.DB_NAME, user=config.DB_USER, password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("select * from stock where is_etf = TRUE")

etfs = cursor.fetchall()

dates = ['2022-04-08']

for current_date in dates:
    for etf in etfs:
        print(etf['symbol'])
        with open(f"data/{current_date}/{etf['symbol']}.csv") as f:
            reader = csv.reader(f)
            for row in reader:
                ticker = row[0]

                if ticker: 
                    
                    weight = row[2]
                    fund = row[4]

                    cursor.execute("""
                        SELECT * FROM stock WHERE symbol = %s
                    """, (ticker,))
                    stock = cursor.fetchone()
                    if stock:
                        print(f"Inserting a holding into {etf['symbol']}")
                        cursor.execute("""
                            INSERT INTO etf_holding (etf_id, holding_id, dt,fund_name,weight)
                            VALUES (%s, %s, %s, %s,%s)
                        """, (etf['id'], stock['id'], current_date, fund,weight))

connection.commit()