'''
Gets text content for tweet IDs
'''

# standard
from __future__ import print_function
import getopt
import logging
import os
import sys
import time
# import traceback
# third-party: `pip install tweepy`
import tweepy

# global logger level is configured in main()
Logger = None

# Generate your own at https://apps.twitter.com/app
CONSUMER_KEY = 'iBNjiQC8CKEUY8UR5Q17cvAOV'
CONSUMER_SECRET = 'C7gftrhGIkg6QVF3eMh9mleb9OYve87LijjEvoHykO17y01UwL'
OAUTH_TOKEN = '715011126598078464-sKlmBWSkgoygj3INvPjQTd6TEZGJLe0'
OAUTH_TOKEN_SECRET = 't2RtvUgSnDBVdaGY1iRGRaDUyiS5I9eeEchx2up3klG9I'

# batch size depends on Twitter limit, 100 at this time
batch_size=100

def get_tweet_id(line):
    '''
    Extracts and returns tweet ID from a line in the input.
    '''
    # (tagid,_timestamp,_sandyflag) = line.split('\t')
    # (_tag, _search, tweet_id) = tagid.split(':')
    tweet_id = line.split()[0]
    return tweet_id

def get_tweets_single(twapi, idfilepath):
    '''
    Fetches content for tweet IDs in a file one at a time,
    which means a ton of HTTPS requests, so NOT recommended.

    `twapi`: Initialized, authorized API object from Tweepy
    `idfilepath`: Path to file containing IDs
    '''
    # process IDs from the file
    with open(idfilepath, 'rb') as idfile:
        for line in idfile:
            tweet_id = get_tweet_id(line)
            Logger.debug('get_tweets_single: fetching tweet for ID %s', tweet_id)
            try:
                tweet = twapi.get_status(tweet_id)
                print('%s' % (tweet.text.encode('UTF-8')))
            except tweepy.TweepError as te:
                Logger.warn('get_tweets_single: failed to get tweet ID %s: %s', tweet_id, te.message)
                # traceback.print_exc(file=sys.stderr)
        # for
    # with

def get_tweet_list(twapi, idlist):
    '''
    Invokes bulk lookup method.
    Raises an exception if rate limit is exceeded.
    '''
    # fetch as little metadata as possible
    tweets = twapi.statuses_lookup(id_=idlist, include_entities=False, trim_user=True)
    # if len(idlist) != len(tweets):
    #     Logger.warn('get_tweet_list: unexpected response size %d, expected %d', len(tweets), len(idlist))
    return tweets
    # for tweet in tweets:
    #     if tweet.lang == 'en':
    #         print('%s' % (tweet.text))

def get_tweets_bulk(twapi, idfilepath, outputname):
    '''
    Fetches content for tweet IDs in a file using bulk request method,
    which vastly reduces number of HTTPS requests compared to above;
    however, it does not warn about IDs that yield no tweet.

    `twapi`: Initialized, authorized API object from Tweepy
    `idfilepath`: Path to file containing IDs
    '''    
    # process IDs from the file
    out = open(outputname, 'w')
    tweet_ids = list()
    with open(idfilepath, 'r') as idfile:
        for line in idfile:
            tweet_id = get_tweet_id(line)
            Logger.debug('Enqueing tweet ID %s', tweet_id)
            tweet_ids.append(tweet_id)
            # API limits batch size
            if len(tweet_ids) == batch_size:
                Logger.debug('get_tweets_bulk: fetching batch of size %d', batch_size)
                tweets = get_tweet_list(twapi, tweet_ids)
                for tweet in tweets:
                    if tweet.lang == 'en':
                        out.write(tweet.text+'\n')
                tweet_ids = list()
    # process remainder
    if len(tweet_ids) > 0:
        Logger.debug('get_tweets_bulk: fetching last batch of size %d', len(tweet_ids))
        tweets = get_tweet_list(twapi, tweet_ids)
        for tweet in tweets:
            if tweet.lang == 'en':
                out.write(tweet.text + '\n')
    out.close()

def usage():
    print('Usage: get_tweets_by_id.py [options] file')
    print('    -s (single) makes one HTTPS request per tweet ID')
    print('    -v (verbose) enables detailed logging')
    sys.exit()

def main():
    logging.basicConfig(level=logging.WARN)
    global Logger
    Logger = logging.getLogger('get_tweets_by_id')
    bulk = True
    # try:
    #     opts, args = getopt.getopt(args, 'sv')
    # except getopt.GetoptError:
    #     usage()
    # for opt, _optarg in opts:
    #     if opt in ('-s'):
    #         bulk = False
    #     elif opt in ('-v'):
    #         Logger.setLevel(logging.DEBUG)
    #         Logger.debug("main: verbose mode on")
    #     else:
    #         usage()
    # if len(args) != 1:
    #     usage()
    # idfile = args[0]
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    api = tweepy.API(auth)

    dates = ["20110123","20110125", "20110126", "20110127", "20110128", "20110129", "20110130", "20110131"]
    for data in dates:
        for filename in os.listdir('./data/'+date):
            if filename[-3:] == 'dat':
                outputname = './data/' +date + '/' + filename[:-4] + '-result.txt'
                idfile = './data/' +date + '/' +  filename
                if os.path.exists(outputname):
                    continue
                if bulk:
                    get_tweets_bulk(api, idfile, outputname)
                else:
                    get_tweets_single(api, idfile)
                print(idfile)
                time.sleep(60)
    print("end of fetching data")

    # idfile = './data/20110123-000.dat'
    # if not os.path.isfile(idfile):
    #     print('Not found or not a file: %s' % idfile, file=sys.stderr)
    #     usage()

    # # connect to twitter
    

    # # hydrate tweet IDs
    # if bulk:
    #     get_tweets_bulk(api, idfile)
    # else:
    #     get_tweets_single(api, idfile)

if __name__ == '__main__':
    main()
