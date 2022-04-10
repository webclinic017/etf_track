from psaw import PushshiftAPI
import datetime
import psycopg2
import psycopg2.extras
import config

connection= psycopg2.connect(host = config.DB_HOST,database=config.DB_NAME,user=config.DB_USER,password=config.DB_PASS)

cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("SELECT * FROM stock")

rows = cursor.fetchall()



stocks = {}
for row in rows:
    stocks['$' + row['symbol']] = row['id']



api = PushshiftAPI()



start_time=int(datetime.datetime(2022, 4, 5).timestamp())

submissions = api.search_submissions(after=start_time,
                                    subreddit='wallstreetbets',
                                    filter=['url','author', 'title', 'subreddit'])

for sub in submissions:
    words = sub.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith("$"),words)))
    if len(cashtags) > 0:
        #print(cashtags)
        #print(sub.created_utc)
        #print(sub.title)
        #print(sub.url)
        for cashtag in cashtags:

            submitted_time = datetime.datetime.fromtimestamp(sub.created_utc).isoformat()
            try:
                cursor.execute('''
                    INSERT INTO mention (dt, stock_id,message,source,url)
                    VALUES (%s,%s,%s,'wallstreetbets',%s)
                ''',(submitted_time,stocks[cashtag],sub.title,sub.url))
                connection.commit()
            except Exception as e:
                print(e)
                connection.rollback()


        