import urllib2, json

class FS(object):
    def __init__(self, settings):
        self.settings = settings

    def FSRegister(self, code, redirecturl):

        if code:
            url = "https://foursquare.com/oauth2/access_token?client_id=%s&client_secret=%s&grant_type=authorization_code&redirect_uri=%s&code=%s" % (
                self.settings['clientid'],
                self.settings['clientsecret'],
                redirecturl,
                code)

            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            data = response.read()
            jdata = json.loads(data)
            return jdata
        else:
            return False