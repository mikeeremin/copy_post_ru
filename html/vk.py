import json, urllib2, urllib
import pycurl, StringIO, os

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
        exts = ('jpg', 'gif', 'JPG', 'jpeg', 'JPEG', 'GIF', 'png', 'PNG')
        url = "https://api.vkontakte.ru/method/wall.post"
        data = {'message': message.encode('utf-8'),
                'access_token': ppobject.access_token,
                'owner_id': -ppobject.userid,
                'from_group': 1}
        if attachments:
            data['attachments'] = []
            for attach in attachments:
                isphoto = False
                for ext in exts:
                    if attach.endswith(ext):
                        params = self.VKGetWallUploadServer(ppobject.access_token, ppobject.userid)
                        if 'response' in params and 'upload_url' in params['response']:
                            photo = self.VKUploadWallPhoto(params['response']['upload_url'], attach,
                                                           ppobject.access_token, ppobject.userid, ext)
                            if photo:
                                data['attachments'].append(photo)
                                isphoto = True
                if not isphoto:
                    data['attachments'].append(attach)
            data['attachments'] = ",".join(data['attachments'])
        resp = urllib2.urlopen(url, urllib.urlencode(data))
        return resp.read()

    def VKGetGroups(self, access_token):
        req = "https://api.vkontakte.ru/method/groups.get?access_token=%s&extended=1" % access_token
        resp = urllib2.urlopen(req)
        groups = json.loads(resp.read())
        return  groups

    def VKGetUserSettings(self, access_token):
        req = "https://api.vkontakte.ru/method/getUserSettings?access_token=%s&extended=1" % access_token
        resp = urllib2.urlopen(req)
        print resp.read()


    def VKGetWallUploadServer(self, access_token, gid):
        req = "https://api.vkontakte.ru/method/photos.getWallUploadServer"
        data = {
            'access_token': access_token,
            'gid': -gid}
        resp = urllib2.urlopen(req, urllib.urlencode(data))
        params = json.loads(resp.read())
        return  params

    def VKUploadWallPhoto(self, url, photo, access_token, gid, ext):
        img = urllib2.urlopen(photo)
        try:
            os.unlink('/tmp/photo.%s' % ext)
        except Exception:
            pass
        local_file = open('/tmp/photo.%s' % ext, "wb")
        local_file.write(img.read())
        buffer = StringIO.StringIO()
        fields = [
            ('photo', (pycurl.FORM_FILE, '/tmp/photo.%s' % ext)),
        ]
        c = pycurl.Curl()
        c.setopt(c.POST, 1)
        c.setopt(c.URL, str(url))
        c.setopt(c.HTTPPOST, fields)
        c.setopt(c.WRITEFUNCTION, buffer.write)

        c.perform()
        c.close()
        params = json.loads(buffer.getvalue())
        if 'server' in params:
            req = "https://api.vkontakte.ru/method/photos.saveWallPhoto"
            data = {
                'access_token': access_token,
                'server': params['server'],
                'photo': params['photo'],
                'hash': params['hash'],
                'gid': -gid}
            resp = urllib2.urlopen(req, urllib.urlencode(data))
            params = json.loads(resp.read())
            if 'response' in params and params['response'][0] and 'id' in params['response'][0]:
                return params['response'][0]['id']
            else:
                return params
        return False
