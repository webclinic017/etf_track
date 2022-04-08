import config
import json
from alpaca_trade_api.rest import REST, TimeFrame,TimeFrameUnit
import psycopg2
import psycopg2.extras
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:password@localhost:5432/etfdb')

connection = engine.connect()

sql = "SELECT * FROM stock WHERE id IN (SELECT holding_id FROM etf_holding)"

stocks = pd.read_sql(sql,connection)
stock_dict = stocks.to_dict('records')


api = REST(config.API_KEY,config.API_SECRET,base_url=config.API_URL)


for r in stock_dict:
    try:
        df = api.get_bars(r['symbol'], TimeFrame(5, TimeFrameUnit.Minute), "2020-10-01", "2022-04-06", adjustment='raw').df
        if len(df) > 0:
            df['stock_id'] = r['id']
            df = df.reset_index()
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df = df.rename(columns={'timestamp':'dt'}).drop(columns=['trade_count','vwap'])
            print(f"Inserting stock price for {r['symbol']}")
            df.to_sql('stock_price',if_exists='append',con=connection,index=False)
    except Exception as e:
        print(e)
