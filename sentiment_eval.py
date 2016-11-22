import json
import re
from sentiment_module import sentiment

fw = open('sentiment_output.json','a')

def sentiment_eval(tweet_text):
    result = sentiment(tweet_text)
    return result

def get_candidate_name(tweet_text):
    trump = ['trump','donald','republicans', 'conservative','maga', 'lockhimup','he','his','pence','racist']
    hillary = ['liberal','hillary','clinton','democrat','lockherup','progessive','her','she','kaine','democratic','left']

    hillary_re = re.compile("|".join(hillary))
    trump_re = re.compile("|".join(trump))

    if hillary_re.search(tweet_text):
        return "hillary"
    elif trump_re.search(tweet_text):
        return "trump"
    else:
        return "None"

with open('data_live6_output_3.json', 'r') as f:
    count = 0
    ncount = 0
    # read tweets line by line
    for line in f:
        try:
            tweet = json.loads(line) # load it as Python dict
            #print tweet.get('tweet_text')
            candidate_name = get_candidate_name(tweet.get('tweet_text'))
            #print candidate_name
            #i = input("continue??")
            if candidate_name == "None":
                ncount += 1
                # if ncount < 10:
                #     print tweet.get('tweet_text')
            else:
                tweet.update({'candidate_name': candidate_name})
                count += 1
                # if count < 10:
                #     print tweet.get('tweet_text')
                sentiment = sentiment_eval(tweet.get('tweet_text'))
                tweet.update({'text_sentiment': sentiment[0]})
                tweet.update({'sentiment_confidence': sentiment[1]})

                #sorting accourding to key fields in dictonary
                order_parsed_tweet = collections.OrderedDict(sorted(tweet.items()))
                #print(json.dumps(order_parsed_tweet, indent=4)) # pretty-print
                fw.write(json.dumps(order_parsed_tweet))
                fw.write("\n")
        except:
            pass
# print count
# print ncount
# sentiment = sentiment_eval(tweet.get('tweet_text'))
# tweet.update({'text_sentiment': sentiment[0]})
# tweet.update({'sentiment_confidence': sentiment[1]})