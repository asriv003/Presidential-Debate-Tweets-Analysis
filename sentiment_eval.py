import json
import re
import sentiment_trained as s
# import sentiment_module as s
import collections
# from sentiment_trained import *

fw = open('sentiment_output.json','a')

def sentiment_eval(tweet_text):
    result = s.sentiment(tweet_text)
    return result
trump_count = 0
hillary_count = 0 

def get_candidate_name(tweet_text):
    trump = ['trump','donald','republicans', 'conservative','maga', 'lockhimup','pence','racist','trump2016','StandByTrump','realDonaldTrump']
    hillary = ['liberal','hillary','clinton','democrat','lockherup','progessive','kaine','democratic','left','hillary2016','IAmWithHer','ImWithHer','HillaryClinton']
    global trump_count, hillary_count
    

    # for word in trump:
    #     if word in tweet_text:
    #         trump_count += 1
    #         return "trump"

    # for word in hillary:
    #     if word in tweet_text:
    #         hillary_count += 1
    #         return "hillary"
    # return "None"
    hillary_re = re.compile("|".join(hillary))
    trump_re = re.compile("|".join(trump))

    if hillary_re.search(tweet_text):
        return "hillary"
    elif trump_re.search(tweet_text):
        return "trump"
    else:
        return "None"

with open('parsed_data/part_aa.json', 'r') as f:
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
                senti = sentiment_eval(tweet.get('tweet_text'))
                tweet.update({'text_sentiment': senti[0]})
                tweet.update({'sentiment_confidence': senti[1]})

                #sorting accourding to key fields in dictonary
                order_parsed_tweet = collections.OrderedDict(sorted(tweet.items()))
                #print(json.dumps(order_parsed_tweet, indent=4)) # pretty-print
                fw.write(json.dumps(order_parsed_tweet))
                fw.write("\n")
        except Exception as e:
            print str(e)
            
print count
print ncount

# print hillary_count
# print trump_count
# sentiment = sentiment_eval(tweet.get('tweet_text'))
# tweet.update({'text_sentiment': sentiment[0]})
# tweet.update({'sentiment_confidence': sentiment[1]})