from psaw import PushshiftAPI
import config_cloud
import datetime
from datetime import timedelta
import psycopg2
import psycopg2.extras

connection = psycopg2.connect(host=config_cloud.DB_HOST_cloud,password=config_cloud.DB_PASS_cloud,database= config_cloud.DB_NAME_cloud,user=config_cloud.DB_USER_cloud,port=config_cloud.DB_PORT_cloud)
cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
cursor.execute("""
    SELECT * FROM hotteststocks
""")
rows = cursor.fetchall()

stocks = {}
for row in rows: 
    stocks['$' + row['symbol']] = row['id']


api = PushshiftAPI()

#start_time = int(datetime.datetime(2022, 3, 26).timestamp())
today = datetime.datetime.today()
yesterday = int((today - timedelta(days=5)).timestamp())

submissions = api.search_submissions(after=yesterday,
                                     subreddit='wallstreetbets',
                                     filter=['url','author', 'title', 'subreddit'])
                                     

for submission in submissions:
    words = submission.title.split()
    cashtags = list(set(filter(lambda word: word.lower().startswith('$'), words)))

    if len(cashtags) > 0:
        print(cashtags)
        print(submission.title)

        for cashtag in cashtags:
            if cashtag in stocks:
                submitted_time = datetime.datetime.fromtimestamp(submission.created_utc).isoformat()

                try:
                    cursor.execute("""
                        INSERT INTO mention_wallstreet (dt, stock_id, message, source, url)
                        VALUES (%s, %s, %s, 'wallstreetbets', %s)
                    """, (submitted_time, stocks[cashtag], submission.title, submission.url))

                    connection.commit()
                except Exception as e:
                    print(e)
                    connection.rollback()

