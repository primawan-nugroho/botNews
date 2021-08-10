#!/usr/bin/env python
# tweepy-bots/bots/followfollowers.py

import tweepy
import logging
import time
import schedule
from gnewsclient import gnewsclient
from config import create_api
from datetime import datetime

########################################
MAX_NEWS = 3
TOPIC = "Sports"
LANGUAGE = "Indonesian"
LOCATION = "Indonesia"
TIME = [None] * MAX_NEWS
TIME[0] = "07:05"
TIME[1] = "07:10"
TIME[2] = "07:15"
########################################

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
item = 0

def check_mentions(api, keywords, since_id):
    logger.info("Retrieving mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            continue
        if any(keyword in tweet.text.lower() for keyword in keywords):
        	try:
        		logger.info(f"Mentioned by: {tweet.user.name}")
        		api.update_status(
                	status="Tweet berita "+TOPIC+" Indonesia "+MAX_NEWS+" kali sehari",
                	in_reply_to_status_id=tweet.id,
                	auto_populate_reply_metadata=True
            	)
        	except tweepy.TweepError as e:
        		print(e.reason)
        		time.sleep(2)
    return new_since_id

def tweet_news(api, item):
	client = gnewsclient.NewsClient(language=LANGUAGE, location=LOCATION, topic=TOPIC, max_results=MAX_NEWS)
	news_list = client.get_news()

	try:
		logger.info("Tweeting...")
		tweet1 = news_list[item]['title']
		tweet2 = news_list[item]['link']
		tweet = tweet1+"\n"+tweet2
		api.update_status(status=tweet)
		logger.info("Tweet Success:\n"+tweet1)
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print("at "+ current_time+"\n")
	except tweepy.TweepError as e:
		print(e.reason)
		time.sleep(2)

def main():
	api = create_api()
	logger.info(f"Authenticated")
	
	for i in range(MAX_NEWS):
		schedule.every().day.at(TIME[i]).do(tweet_news, api, i)

	while True:
		schedule.run_pending()
		time.sleep(1)

if __name__ == "__main__":
    main()