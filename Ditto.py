import tweepy
import json
import time
import re
# Twitter API credentials
consumer_key = "NkQPzpiRJZ6CJVeRzrVLqIGuh"
consumer_secret = "yMhadrMcNmAQyFGX8YKDWtyX6szbr3hKGwCKrz9xp36KPI7tMX"
access_key = "1066866967-dDLwsuOq4YdKRm1v1v4lbzWlu3rTMvPoS8TYjWG"
access_secret = "FiC4HGQDEInch3tar4nGDwpApxcwI2KesP85h3JXOX5fo"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

data = api.search("#TeamJB", count=2, tweet_mode='extended', result_type='recent')

# tweet_hashtags = [t['text'] for t in tweet._json['entities']['hashtags'] for tweet in data]

# raw_tags = [tweet._json['entities']['hashtags'] for tweet in data]

# tags = [print(t['text']) for t in raw_tags  if len(t) > 0]
# print(tweet_hashtags)

# for tweet in api.search("#TeamJB", count=1, tweet_mode='extended', result_type='recent'):
#     print(json.dumps(tweet._json['user'], indent=4))
# print(api.search("#TeamJB", count=1, tweet_mode='extended')['source_url'])
# print(json.dumps(tweepy.Cursor(api.search, q='#TeamJB', count=1, tweet_mode='extended')), indent=2)
# print(json.dumps(api.search("#TeamJB", count=1, tweet_mode='extended').items()), indent=2)
# def valid(tweet):
#     if tweet._json['user']['followers_count'] < 100:
#         return False
#     if not re.search(r'(chicago)|(il)|(illinois)',tweet._json['user']['location'], re.I):
#         return False
#     return True
#
#
# def handle_tweet(tags, base_name, user_id, user_screen_name):
#     hashtags = {}
#     for tag in tags:
#         if tag not in hashtags:
#             hashtags[base_name][tag] = {
#                 'name': tag,
#                 'users': {
#                     user_id: {
#                         'user_id': user_id,
#                         'user_screen_name': user_screen_name,
#                         'count': 1
#                     }
#                 }
#             }
#         else:
#             if user_id in hashtags[base_name][tag]['users']:
#                 hashtags[base_name][tag]['users'][user_id]['count'] = hashtags[base_name][tag]['users'][user_id]['count'] + 1
#             else:
#                 hashtags[base_name][tag]['users'][user_id] = {
#                     'user_id': user_id,
#                     'user_screen_name': user_screen_name,
#                     'count': 1
#                 }
#     return hashtags
#
#
# def check_limit():
#     if api.rate_limit_status()['resources']['search']['/search/tweets']['remaining'] < 5:
#         sleepy_time = api.rate_limit_status()['resources']['search']['/search/tweets']['reset'] - time.time()
#         print('Rate limit reached.... sleeping for ', sleepy_time/60, ' minutes')
#         time.sleep(sleepy_time)
#
#
# def parse_networks(networks, count=100):
#     try:
#         hashtags = {}
#         users = {}
#
#         # initialize data structures
#         for val in networks:
#             hashtags[val] = {}
#
#         for network in networks:
#             for tweet in tweepy.Cursor(api.search, q=network, count=count, tweet_mode='extended').items():
#                 check_limit()
#                 if valid(tweet):
#                     user_id = tweet._json['user']['id']
#                     user_screen_name = tweet._json['user']['screen_name']
#                     tweet_hashtags = [t['text'] for t in tweet._json['entities']['hashtags']]
#                     if len(tweet_hashtags) > 0:
#                         for tag in tweet_hashtags:
#                             if tag not in hashtags[network]:
#                                 hashtags[network][tag] = {
#                                     'name': tag,
#                                     'users': {
#                                         user_id: {
#                                             'user_id': user_id,
#                                             'user_screen_name': user_screen_name,
#                                             'count': 1
#                                         }
#                                     }
#                                 }
#                             else:
#                                 if user_id in hashtags[network][tag]['users']:
#                                     hashtags[network][tag]['users'][user_id]['count'] = hashtags[network][tag]['users'][user_id]['count'] + 1
#                                 else:
#                                     hashtags[network][tag]['users'][user_id] = {
#                                         'user_id': user_id,
#                                         'user_screen_name': user_screen_name,
#                                         'count': 1
#                                     }
#
#         print(json.dumps(hashtags, indent=2))
#     except Exception as e:
#         print(e)
#
#
# print(api.rate_limit_status()['resources']['search'])
# parse_networks(['#TeamJB', '#TeamRauner'], count=4)
# parse_networks(['#TeamJB'], count=3)
# check_limit()
# print(api.rate_limit_status()['resources']['search'])
#

# user_id = tweet._json['id']
# user_screen_name = tweet._json['user']['screen_name']
# user_location = tweet._json['user']['location']
# user_protected = tweet._json['user']['protected']
# user_followers = tweet._json['user']['followers_count']
#
# user_mentions = [{'mentioned_id': t['id'], 'mentioned_screen_name': t['screen_name']} for t in tweet._json['entities']['user_mentions']]
# tweet_hashtags = [t['text'] for t in tweet._json['entities']['hashtags']]

