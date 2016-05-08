#! python3

import tweepy, random
from tkdTweets_Lib import * #library of tweets GW created
from tkdTrainingTweets import *
from tweetKeys import * #twitter dev keys GW created
from datetime import datetime
from time import sleep
import schedule, time, sched

auth = tweepy.OAuthHandler (consumerKey, consumerSecret)
auth.set_access_token (accessKey, accessSecret)
api = tweepy.API(auth)

def tkdTwitterBot():
    try:
        n = 0
        while n <= 3:
            print('Tweeted on:', datetime.today())
            Tweet = random.choice (tkdTweets) #local variable - needs to be inside the variable to gen random tweet on each iteration
            api.update_status (Tweet)
            n+=1
            sleep(600) #works with datetime without time.sleep after importing from datetime

    except tweepy.TweepError:
            "'message': 'Status is a duplicate.', 'code': 187"
            print ('Twitter Error Occured ', datetime.today())


##################################################################################
##################################################################################
#Training Day Twitter Bot
#Has it's own Library tkdTrainingTweets

def tkdTrainingDayBot():
    try:
        print('Tweeted on:', datetime.today())
        Tweet = random.choice (trainingDayTweet) #local variable - needs to be inside the variable to gen random tweet on each iteration
        api.update_status (Tweet)    

    except tweepy.TweepError:
            "'message': 'Status is a duplicate.', 'code': 187"
            print ('Twitter Error Occured ', datetime.today())
            tkdTwitterBot()

#################################################################################
#################################################################################
#TKD Follower Bot

searchTerms = ['#norwich', 'martial arts', 'taekwondo', 'Taekwon-Do', '#fitness', '#mondaymotivation', 'uea']
to_follow = []

auth = tweepy.OAuthHandler (consumerKey, consumerSecret)
auth.set_access_token (accessKey, accessSecret)
api = tweepy.API(auth)

public_tweets = api.home_timeline()
user = api.get_user ('NorwichTKD')

#Date Variable to gen today's date and then -7 days

today = datetime.today()
day = today.strftime ('%Y''-''%m''-''%d')
negSeven = today - timedelta(7)

runDay = day
sevenDays = negSeven.strftime ('%Y''-''%m''-''%d')

#for search in searchTerms:
 #   print (search)

def findFollowers ():
    try:
        for search in searchTerms:
            for tweet in tweepy.Cursor(api.search, q= search, since=str(sevenDays), until=str(runDay)).items(150):
                to_follow.append(tweet.user.screen_name)
                #print (to_follow)

        for friends in to_follow:
            api.create_friendship (friends)
            print (friends)

    except tweepy.TweepError:
        "'message': \"You are unable to follow more people at this time. Learn more <a href='http://support.twitter.com/articles/66885-i-can-t-follow-people-follow-limits'>here</a>.\", 'code': 161"
        print ('Unable to follow more people at this time. Sleeping for 1 hour')
        sleep (60*60)

    except tweepy.TweepError:
        "'code': 158, 'message': \"You can\'t follow yourself.\""
        print ('Unable to follow yourself error.')

#################################################################################
#################################################################################
#Schedule Function.

task = sched.scheduler (time.time, time.sleep)


schedule.every().monday.at('17:15').do(tkdTrainingDayBot())
schedule.every().tuesday.at('18:30').do(tkdTwitterBot())
schedule.every().wednesday.at('17:10').do(tkdTrainingDayBot())
schedule.every().friday.at('18:00').do(tkdTwitterBot())
schedule.every().saturday.at('13:00').do(tkdTwitterBot())
schedule.every().sunday.at('13:00').do(findFollowers())

while True:
    schedule.run_pending()
    time.sleep (1)
