import json, urllib2, urllib

class VK(object):
    def __init__(self, settings):
        self.settings = settings


    #
    # VKRegister(code)
    # return access_token
    #
    def VKRegister(self, code):
        if code:
            url = "https://api.vkontakte.ru/oauth/access_token?client_id=%s&client_secret=%s&code=%s" % (
                self.settings['VKONTAKTE_CLIENT_ID'],
                self.settings['VKONTAKTE_CLIENT_SECRET'],
                code)
            req = urllib2.Request(url)
            response = urllib2.urlopen(req)
            data = response.read()
            jdata = json.loads(data)
            return jdata
        else:
            return False


    def VKGetWall(self, ppobject, count):
        url = "https://api.vkontakte.ru/method/wall.get"
        data = {'access_token': ppobject.access_token,
                'owner_id': -ppobject.userid,
                'count': count}

        resp = urllib2.urlopen(url, urllib.urlencode(data))
        posts = json.loads(resp.read())
        return  posts

    def VKPost(self, ppobject, message, attachments=None):
        url = "https://api.vkontakte.ru/method/wall.post"
        data = {'message': message.encode('utf-8'),
                'access_token': ppobject.access_token,
                'owner_id': -ppobject.userid,
                'from_group': 1}

        if attachments:
            data['attachments'] = ",".join(attachments)
        resp = urllib2.urlopen(url, urllib.urlencode(data))
        print resp.read()

    #        if urllib2.urlopen(url, urllib.urlencode(data)):
    #            return True
    #        else:
    #            return False

    def VKGetGroups(self, access_token):
        
        req = "https://api.vkontakte.ru/method/groups.get?access_token=%s&extended=1" % access_token
        resp = urllib2.urlopen(req)
        groups = json.loads(resp.read())
        return  groups

    def VKGetUserSettings(self, access_token):
        req = "https://api.vkontakte.ru/method/getUserSettings?access_token=%s&extended=1" % access_token
        resp = urllib2.urlopen(req)
        print resp.read()