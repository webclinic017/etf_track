from alpaca_trade_api.stream import Stream
import config

async def trade_callback(t):
    print('trade', t)


async def quote_callback(q):
    print('quote', q)


# Initiate Class Instance
stream = Stream(config.API_KEY,
                config.API_SECRET,
                base_url=config.API_URL,
                data_feed='iex')  # <- replace to SIP if you have PRO subscription

# subscribing to event
stream.subscribe_trades(trade_callback, 'TSLA')
stream.subscribe_quotes(quote_callback, 'GOOG')
stream.subscribe_quotes(quote_callback, 'YETI')

stream.run()