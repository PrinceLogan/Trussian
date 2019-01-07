#!/usr/bin/python3
#from __future__ import absolute_import, print_function
from CredData import * #API Credentials are matinaed in a seperate file
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy

from yandex_translate import YandexTranslate

auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth)

translate = YandexTranslate(YandexKey)

def from_creator(status): #By default, tweepy includes retweets in stream.filter(follow= We only want to handle status updates
    if hasattr(status, 'retweeted_status'):
        return False
    elif status.in_reply_to_status_id != None:
        return False
    elif status.in_reply_to_screen_name != None:
        return False
    elif status.in_reply_to_user_id != None:
        return False
    else:
        return True

class StdOutListener(StreamListener):
    def on_status(self, status):
        if from_creator(status):
            try: 
                message = status.text
                trussy = translate.translate(message, 'en-ru') #Select the lanague you are translating from-to
                x = trussy["text"]
                for x in x:
                    print(x)
                    api.update_status(x)
                return True
            except BaseException as e:
                print("Error on_data %s" % str(e))
            return True
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    l = StdOutListener()
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    stream = Stream(auth, l)
stream.filter(follow=['25073877']) #Enter the Twitter ID of the user to monitor
