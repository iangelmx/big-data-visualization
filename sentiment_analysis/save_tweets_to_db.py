import sys
sys.path.append('./../')
from libs.tweets_getter import ( get_analytics_for_search,
                                 merge_tweets_to_translated_text)
from libs.mongo_lib import Bd

tweets_records, en_tweets = get_analytics_for_search(
    search_text='Resuelve', 
    limit_tweets=200, 
    translate_to_en=True
)

#Get the records with original and translated tweet
records = merge_tweets_to_translated_text( tweets_records, en_tweets )

bd = Bd('localhost', 'aramirez', 'iangelmx', 'test')

for a in records:
    print(a)
    print("\n\n\n\n")


print(bd.insert_in_db('tweets_resuelve', list(records)))