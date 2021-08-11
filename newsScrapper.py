#for testing without tweeting
from gnewsclient import gnewsclient
import schedule
import time

def print_news():
    client = gnewsclient.NewsClient(
        language='Indonesian',
        location='Indonesia',
        topic='Nation',
        max_results=3
    )
    # get news feed
    news_list = client.get_news()
    #for item in news_list:
    #    print(item['title'])
    print(news_list[0]['title'])

schedule.every(1).minutes.do(print_news)

while True:
    schedule.run_pending()
    time.sleep(1)
