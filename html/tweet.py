import tweepy
import cgi
import oauth2
import twitter, urllib


class Tweet(object):
    consumer_key = None
    consumer_secret = None
    handler = None

    def __init__(self, settings):
        self.settings = settings

    def login(self, access_token, access_secret):
        self.handler = twitter.Api(
            self.settings['CONSUMER_KEY'],
            self.settings['CONSUMER_SECRET'],
            access_token,
            access_secret
        )

    #TIME_LINE
    def get_tl(self):
        try:
            return self.handler.GetUserTimeline("Zl0n1k")
        except Exception, err:
            return False

    def post(self, msg):
        try:
            self.handler.PostUpdate(msg)
            return True
        except Exception, err:
            return False


    def register(self, oauth_token=None, oauth_secret=None, pin=None, callbackurl = None):
        #CONSUMER
        oauth_consumer = oauth2.Consumer(key=self.settings['CONSUMER_KEY'], secret=self.settings['CONSUMER_SECRET'])

        if oauth_token:
            #REGISTER FINAL STEP
            token = oauth2.Token(oauth_token, oauth_secret)
            token.set_verifier(pin)
            oauth_client = oauth2.Client(oauth_consumer, token)
            resp, content = oauth_client.request(self.settings['ACCESS_TOKEN_URL'], method='POST', body='oauth_verifier=%s' % pin)
            access_token = dict(cgi.parse_qsl(content))

            #CHECK RESPONSE
            if resp['status'] != '200':
                return False
            else:
                return access_token
        else:
            #REGISTER FIRST STEP
            oauth_client = oauth2.Client(oauth_consumer)
            resp, content = oauth_client.request(self.settings['REQUEST_TOKEN_URL'], 'POST', body='oauth_callback=%s' % callbackurl)
            
            #CHECK RESPONSE
            if resp['status'] != '200':
                return False
            else:
                request_token = dict(cgi.parse_qsl(content))
                return {"url": "%s?oauth_token=%s" % (self.settings['AUTHORIZATION_URL'], request_token['oauth_token']),
                        "data": request_token}






