import tweepy
from textblob import TextBlob
import sys
import unicodecsv as csv
import read_csv

if len(sys.argv) >= 2:
    topic = sys.argv[1]
else:
    print('By default topic is Smite')
    topic = 'Smite'


consumer_key = 'ENTER-THIS-KEY'
consumer_secret = 'ENTER-THIS-SECRET'

access_token = 'ENTER-THIS-TOKEN'
access_token_secret = 'ENTER-THIS-SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)

api = tweepy.API(auth)

public_tweets = api.search('@SmiteGame')
positivecount = 0.0
negativecount = 0.0
tweetcount = 0.0
with open('sentiment.csv', 'wb') as f:

    writer = csv.DictWriter(f, fieldnames=['Tweet','Sentiment'])
    writer.writeheader()
    for tweet in public_tweets:
        text = tweet.text
        csvtext = text.replace('\n','')
        cleanedtext = ' '.join([word for word in text.split(' ') if len(word) > 0 and word[0] != '@' and word[0] != '.'
                                and word[0] != '#' and 'http' not in word and word != 'RT'])
        tweetcount += 1
        analysis = TextBlob(cleanedtext)
        sentiment = analysis.sentiment.polarity
        if sentiment >= 0:
            polarity = 'Positive'
            positivecount += 1
        else:
            polarity = 'Negative'
            negativecount += 1

        writer.writerow({'Tweet':csvtext,'Sentiment':polarity})

with open('sentimentstats.csv','wb') as s:
    writer = csv.DictWriter(s,fieldnames=['Percent','Sentiment'])
    writer.writeheader()
    writer.writerow({'Percent': int(positivecount/tweetcount*100), 'Sentiment': 'Positive Percent'})
    writer.writerow({'Percent': int(negativecount / tweetcount*100), 'Sentiment': 'Negative Percent'})

readnew = raw_input('Would you like to read csv? (y or n)')

if readnew == 'y':
    read_csv.readcsv('sentiment.csv')
    read_csv.readcsv('sentimentstats.csv')
else:
    sys.exit()
