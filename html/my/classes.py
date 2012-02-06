# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from my.models import Sync, PostPlace, SNType
from django.core.urlresolvers import reverse
from my.views import vkauth, fbauth, twauth
from settings import twitter_settings, vk_settings, fb_settings


class Source(object):
    def __init__(self, sntype, request):
        self.sntype = sntype
        self.request = request

    def processSource(self):
        #rss feed
        fields = None
        if self.sntype.code == 'rss':
            if self.request.POST:
                pp = PostPlace()
                pp.sn_type = SNType.objects.get(code='rss')
                pp.url = self.request.POST['feedurl']
                pp.user = self.request.user
                pp.save()
                s = Sync()
                s.source = pp
                s.user = pp.user
                s.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[s.id]))

            fields = [
                    {'name': 'feedurl', 'type': 'text', 'size': 50, 'label': 'Feed URL'},
                    {'name': 'testfeed', 'type': 'button', 'size': 5, 'value': 'Test feed', 'onclick': 'feedtest();'},
                    {'name': 'testfeedresult', 'type': 'alertdiv'},
                    {'name': 'feeduptime', 'type': 'select', 'values': [{'value': 30, 'name': '30 min'}],
                     'label': 'Refresh time'},
                    {'name': 'feedsave', 'type': 'submit', 'value': 'Save feed'},
            ]

        # vkontakte
        if self.sntype.code == 'vk':
            pp = vkauth(self.request)
            if pp:
                s = Sync()
                s.source = pp
                s.user = pp.user
                s.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[s.id]))

            fields = [
                    {'name': 'vkauth', 'type': 'button', 'size': 5, 'value': 'Авторизация через сайт Vkontakte',
                     'onclick': 'vkontakteauth(\'%s%s?%s\');' % (HTTP_HOST, reverse('my.views.new'), 'src=vk')},
            ]

        # twitter
        if self.sntype.code == 'twitter':
            pp = twauth(self.request)
            if pp:
                s = Sync()
                s.source = pp
                s.user = pp.user
                s.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[s.id]))
            tw = Tweet(twitter_settings)
            register = tw.register(
                callbackurl="%s%s?src=twitter" % (HTTP_HOST, reverse('my.views.new')))
            request.session['oauth_token_secret'] = register['data']['oauth_token_secret']
            request.session['oauth_token'] = register['data']['oauth_token']
            fields = [
                    {'name': 'twauth', 'type': 'button', 'size': 5, 'value': 'Twitter auth',
                     'onclick': 'twitterauth(\'%s?src=twitter\', \'%s\');' % (
                         reverse('my.views.new'), register['url'])},
            ]

        #facebook
        if self.sntype.code == 'fb':
            pp = fbauth(request)
            if pp:
                s = Sync()
                s.source = pp
                s.user = pp.user
                s.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[s.id]))

            fb_settings['redirect_uri'] = "%s%s?src=fb" % (HTTP_HOST, reverse('my.views.new'))
            fb = FB(fb_settings)
            url = fb.register()

            fields = [
                    {'name': 'fbauth', 'type': 'button', 'size': 5, 'value': 'Авторизоваться через Facebook',
                     'onclick': 'facebookauth(\'%s\');' % url},
            ]

        return {'fileds' : fields}
    