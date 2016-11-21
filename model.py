from mongokit import Connection, Document
import datetime


MONGO_HOST = '127.0.0.1'
MONGO_PORT = 27017

connection = Connection(MONGO_HOST, MONGO_PORT)


@connection.register
class Tweets(Document):

    __database__ = 'twitter'
    __collection__ = 'tweets'
    structure = { 
            'created_at': unicode,
            'favorite_count': int, 
            'hash_tags': list, 
            'in_reply_to_screen_name': unicode, 
            'in_reply_to_status_id': int, 
            'in_reply_to_user_id': int, 
            'place_coordinates': list, 
            'place_country': unicode, 
            'place_full_name': unicode, 
            'place_type': unicode, 
            'quoted_status_id': int, 
            'retweet_count': int, 
            'timestamp_ms': unicode, 
            'tweet_coordinates': dict, 
            'tweet_id': int, 
            'tweet_source': unicode, 
            'tweet_text': unicode, 
            'user_description': unicode, 
            'user_followers_count': int, 
            'user_friends_count': int, 
            'user_id': int, 
            'user_location': unicode, 
            'user_mentions': list, 
            'user_name': unicode, 
            'user_screen_name': unicode, 
            'user_verified': bool,
            'candidate_name': unicode,
            'text_sentiment': int,
            'sentiment_confidence': float
        }

    use_dot_notation = True
    def __repr__(self):
        return '<Tweets %r>' % (self.tweet_text)
