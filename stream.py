from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

API_KEY = # add api_key from twitter account
SECRET_KEY = # add secret_key from twitter account

ACCESS_TOKEN = # add access token
ACCESS_TOKEN_SECRET = # add secret token 


#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        print data
        return True

    def on_error(self, status):
        print status


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(API_KEY, SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(track=['presidentialdebate', 'hillary2016', 'debate', 'trump', 'hillary', 'debates', 'trump2016'])