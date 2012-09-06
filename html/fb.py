#!/usr/bin/env python
import urllib
import cgi
import facebook


OAUTH_URL = "https://www.facebook.com/dialog/oauth/?"
ACCESS_TOKEN = "https://graph.facebook.com/oauth/access_token?"
ROOT_URL = "https://graph.facebook.com/"

class FB(object):
    settings = None
    auth_params = None
    fb_graph = None

    def __init__(self,settings,code=None):
        self.settings = settings
        self.settings["code"] = code
        self.facebook = facebook


    #REG URL
    def register(self):
        params = {
            "scope": self.settings["permission"],
            "client_id": self.settings["client_id"],
            "client_secret" : self.settings["client_secret"],
            "redirect_uri" : self.settings["redirect_uri"]
        }
        url = OAUTH_URL + urllib.urlencode(params)
        return url

    #LOGIN
    def login(self):
        params = {
            "client_id" : self.settings["client_id"],
            "client_secret" : self.settings["client_secret"],
            "redirect_uri" : self.settings["redirect_uri"],
            "code" : self.settings["code"]
        }
        #raise Exception, params
        access_url = ACCESS_TOKEN + urllib.urlencode(params)
        #raise Exception, access_url
        data = cgi.parse_qs(urllib.urlopen(access_url).read())
        #raise Exception, data
        try:
            self.settings["access_token"] = data["access_token"][0]
            self.fb_graph = facebook.GraphAPI(self.settings["access_token"])
            return True
        except Exception:
            raise Exception, "Can't login to facebook"
        return False

    def sendRequest(self,api_path="",post_params={}):
        data = None
        request_url = ROOT_URL + api_path + "?access_token=" + self.settings["access_token"]
        if post_params:
            data = urllib.urlopen(request_url,urllib.urlencode(post_params)).read()
        else:
            data = urllib.urlopen(request_url).read()
        return data


    #USER INFO
    def getUserInfo(self):
        return self.fb_graph.get_object("me")


    def wallPost(self,message,params={},profile_id="me"):
        post_params = {
            "from": self.settings["post_from"]
        }
        post_params.update(params)
        try:
            ret = self.fb_graph.put_wall_post(message=message,attachment=post_params,profile_id=profile_id)
        except Exception:
            return True
        return ret

    def getGroups(self):

        data = self.fb_graph.get_connections("me","groups")
        return data["data"]

    def getPages(self):
        pages = []
        data = self.fb_graph.get_connections("me","accounts")
        if 'data' in data:
            for a in data['data']:

                if 'perms' in a and 'CREATE_CONTENT' in a['perms']:
                    pages.append(a)
        return pages


    def getGroupFeed(self,group_id):
        return self.fb_graph.get_object("%s/feed" % group_id)["data"]


