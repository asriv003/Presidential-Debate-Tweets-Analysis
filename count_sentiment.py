import json

result = {}
hillary_pos_count = 0
hillary_neg_count = 0
trump_pos_count = 0
trump_neg_count = 0

with open('sentiment_output.json','r') as f:
    for line in f:
        tweet = json.loads(line)
        candidate = tweet.get('candidate_name', None)
        sentiment = tweet.get('text_sentiment', None)
        confidence = tweet.get('sentiment_confidence', None)

        if sentiment == 'pos':
            if candidate == 'hillary':
                hillary_pos_count += 1
            elif candidate == 'trump':
                trump_pos_count += 1
        elif sentiment == 'neg':
            if candidate == 'hillary':
                hillary_neg_count += 1
            elif candidate == 'trump':
                trump_neg_count += 1


print "Hillary Positive: ", str(hillary_pos_count)
print "Hillary Negative: ", str(hillary_neg_count)
print "Trump Positive: ", str(trump_pos_count)
print "Trump Negative: ", str(trump_neg_count)