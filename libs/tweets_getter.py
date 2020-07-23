#In[1]:
import tweepy
import json
from googletrans import Translator
from collections import deque
from typing import Union

settings = json.loads( open('settings.json').read() )

CUSTOMER_KEY = settings['twitter']['customer_key']
CONSUMER_SECRET = settings['twitter']['consumer_secret']

A_TOKEN = settings['twitter']['access_token']
A_T_SECRET = settings['twitter']['access_token_secret']

#In[2]:
auth = tweepy.OAuthHandler(CUSTOMER_KEY, CONSUMER_SECRET)
auth.set_access_token(A_TOKEN, A_T_SECRET)

api = tweepy.API(auth)

#In[19]:
def get_full_text_tweet( tweet ) -> str:
    """Get the full text of a single tweet"""
    try:
        return tweet.retweeted_status.full_text
    except AttributeError:
        #print("No attribute rewtweeted_Status----------------------------")
        return tweet.full_text

#In[18]:
def format_tweet_dict( tweet ) -> dict:
    tweet_dict = {
        'created_at':tweet.created_at,
        'type' : 'retweet',
        'likes' : tweet.favorite_count,
        'rts' : tweet.retweet_count,
        'text' : get_full_text_tweet( tweet )
    }
    
    return tweet_dict
   
#In[21]:
def make_dict_tweet( tweet: tweepy.models.Status  ) -> dict:
    """This function only format the tweepy status to a simple dict to get only
    the interest data."""
    tweet_dict = {
        'created_at':tweet.created_at
    }
    try:
        tweet_dict['text'] = get_full_text_tweet( tweet )
        tweet_dict['type'] = 'retweet'
        tweet_dict['likes'] = tweet.retweeted_status.favorite_count
        tweet_dict['rts'] = tweet.retweeted_status.retweet_count
    except AttributeError:  # Not a Retweet
        tweet_dict['text'] = get_full_text_tweet( tweet )
        tweet_dict['type'] = 'tweet'
        tweet_dict['likes'] = tweet.retweet_count
        tweet_dict['rts'] = tweet.favorite_count
    return tweet_dict

#In[15]:
def get_analytics_for_profile( nickname_user:str, limit_tweets :int = 30, translate_to_en:bool = False ) -> tuple:
    """Get some tweets of a specific profile in Twitter."""
    #nickname_user = 'realDonaldTrump'

    #We will analyze and save the Donald Trump tweets.
    user_id_analyze = api.get_user( nickname_user ).id_str
    #Get the tweets of the public account
    tweets = api.user_timeline(user_id=user_id_analyze, count= limit_tweets, exclude_replies=False, tweet_mode='extended')
    #Transform the tweets in simple dict with the data that we just need
    records = list( map( make_dict_tweet, tweets ) )
    if translate_to_en == True:
        original_tweets_text = list( map( get_full_text_tweet, tweets ) )
        en_tweets_text = translate_text_to_english( original_tweets_text )
        return records, en_tweets_text

    return records

#In[16]:
def get_analytics_for_search( search_text:str, limit_tweets:int = 30, translate_to_en:bool = False ) -> tuple:
    """Get some tweets for a specific search in Twitter"""
    tweets = api.search(q=search_text, tweet_mode='extended', count= limit_tweets)
    tweets_dict = tuple( map( format_tweet_dict, tweets ) )
    if translate_to_en == True:
        original_tweets_text = list( map( get_full_text_tweet, tweets ) )
        en_tweets_text = translate_text_to_english( original_tweets_text )
        return tweets_dict, en_tweets_text

    return tweets_dict

#In[17]:
def translate_text_to_english( sentences : list ) -> tuple:
    """Translate a list of a sentences to english"""
    translator = Translator()
    translations = translator.translate( sentences , dest='en')
    return tuple([ trans.text for trans in translations ])

#In[20]:
def merge_tweets_to_translated_text( tweets_list: Union[list, tuple], setences:list ) -> tuple:
    merged_tweets = tuple( map( lambda tweet, trans: tweet.update({'translated':trans}) or tweet, tweets_list, setences ) )
    return merged_tweets

# %%
# if __name__ == "__main__":
#     # If we want to get tweets of specific profile, use *_for_profile()
#     # a,b = get_analytics_for_profile()

#     # If we want to get tweets of a search text, use *_for_search()
#     tweets_records, en_tweets = get_analytics_for_search('Mexicana de aviación', limit_tweets=5, translate_to_en=True)

#     #Get the records with original and translated tweet
#     records = merge_tweets_to_translated_text( tweets_records, en_tweets )
#     print(records)
    
    

# %%
