import json
import sys
import collections

f = open('parsed_data', 'w')

# if len(sys.argv) > 1:
#     line_generator = open(sys.argv[1])
# else:
#     line_generator = sys.stdin
# for line in line_generator:
#     ### analyze line ###


def parse_and_insert(tweet):
    #parsed tweet
    if tweet['is_quote_status'] and 'quoted_status' in tweet:
        #Insert quoted status
        parse_and_insert(tweet['quoted_status'])
    parsed_tweet = {'created_at': tweet['created_at']}
    parsed_tweet.update({'tweet_id': tweet['id']})
    parsed_tweet.update({'tweet_text': tweet['text']})
    parsed_tweet.update({'tweet_source': tweet['source']})
    parsed_tweet.update({'in_reply_to_status_id': tweet['in_reply_to_status_id']})
    parsed_tweet.update({'in_reply_to_user_id': tweet['in_reply_to_user_id']})
    parsed_tweet.update({'in_reply_to_screen_name': tweet['in_reply_to_screen_name']})
    parsed_tweet.update({'tweet_coordinates': tweet['coordinates']})
    #check if is_quoted_status is true but no quoted_status object is present
    if tweet['is_quote_status'] and 'quoted_status' in tweet:
        parsed_tweet.update({'quoted_status_id': tweet['quoted_status_id']})
    else:
        parsed_tweet.update({'quoted_status_id': 0})
    
    parsed_tweet.update({'retweet_count': tweet['retweet_count']})
    parsed_tweet.update({'favorite_count': tweet['favorite_count']})
    if 'timestamp_ms' in tweet:
        parsed_tweet.update({'timestamp_ms': tweet['timestamp_ms']})
    else:
        parsed_tweet.update({'timestamp_ms': "0"})
    #Users Object
    parsed_tweet.update({'user': tweet['user']})
    #Places Object
    parsed_tweet.update({'place': tweet['place']})
    #Entities Object
    parsed_tweet.update({'entities': tweet['retweet_count']})
    #sorting accourding to key fields in dictonary
    od_parsed_tweet = collections.OrderedDict(sorted(parsed_tweet.items()))

    print(json.dumps(od_parsed_tweet, indent=4)) # pretty-print
    #f.write(json.dumps(od_parsed_tweet))
    return;


with open('test_sample.json', 'r') as f:
    # read tweets line by line
    for line in f:
        tweet = json.loads(line) # load it as Python dict
        parse_and_insert(tweet)
    # try:
    #     actor_id_string = line_object["actor"]["id"]
    #     actor_id = int( actor_id_string.split(":")[2] )
    #     language_code = line_object["twitter_lang"]
    # except KeyError, e:
    #     actor_id = -1
    #     language_code = "Null"

#coordinates - Coordinates object
#place - Places object
#quoted_status - Tweet object
#entities - Entities object
