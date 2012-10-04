# -*- coding: utf-8 -*-
from decorators import render_to
from my.models import PostPlace, Sync, SNType, PostItem, UserProfile
from settings import twitter_settings, HTTP_HOST, fb_settings, vk_settings, fs_settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
import feedparser
from django.core.urlresolvers import reverse
import urllib2, json, re, urllib, md5
from tweet import Tweet
from django.contrib.auth.decorators import login_required
from fb import FB
from vk import VK
from foursquare import FS
from django.shortcuts import redirect

vk_notice = """
Поскольку сайт vkontakte временно или навечно поломал свой API, нужно немного поработать руками.<br>
Щаг 1: Нажать кнопку авторизации через контакт. Согласиться и получить токен.<br>
Выглядит он как набор букв-цифр. access_token=xxxx&другие параметры.<br>
Нужно скопировать в буфер только xxx до знака &.<br>
Вставить его в поле token и сохранить.<br>
<br>
Надеемся, эта мера временная.
"""
lj_notice = """
Мы храним пароль в виде md5-хеша. Хоть насколько-то секьюрно.
"""

@login_required()
@render_to('my/index.html')
def index(request):
    if not request.user:
        return HttpResponseRedirect(reverse('registration.views.login'))
    syncs = Sync.objects.filter(user=request.user)
    for sync in syncs:
        posts = PostItem.objects.filter(pp=sync.source).order_by('-posted')[:5]
        sync.posts = posts
    return {'syncs': syncs}


@login_required()
@render_to('my/new.html')
def new(request):
    if not request.user:
        return HttpResponseRedirect(reverse('registration.views.login'))
    source = None
    fields = None
    sn_types = SNType.objects.all()
    if 'src' in request.GET:
        source = request.GET['src']

        #rss feed
        if source == 'rss':
            error = 0
            if request.POST:
                response = str(feedtest(request))

                if response.find('Feed ok') == -1:
                    error = 1
                else:
                    pp = PostPlace()
                    pp.sn_type = SNType.objects.get(code='rss')
                    pp.url = request.POST['feedurl']
                    pp.user = request.user
                    pp.save()
                    s = Sync()
                    s.source = pp
                    s.user = pp.user
                    s.save()
                    return HttpResponseRedirect(reverse('my.views.sync', args=[s.id]))

            fields = [
                    {'name': 'feedurl', 'type': 'text', 'size': 50, 'label': 'Feed URL', 'sort': 0},
                #{'name': 'feederror', 'type': 'error', 'message': '!!!!!'},
                    {'name': 'testfeed', 'type': 'button', 'size': 5, 'value': 'Test feed', 'onclick': 'feedtest();',
                     'sort': 3},
                    {'name': 'testfeedresult', 'type': 'alertdiv', 'sort': 4},
                    {'name': 'feeduptime', 'type': 'select', 'values': [{'value': 30, 'name': '30 min'}],
                     'label': 'Refresh time', 'sort': 5},
                    {'name': 'feedsave', 'type': 'submit', 'value': 'Далее', 'sort': 6},
                ]
            if error:
                import operator

                fields.append({'name': 'feederror', 'type': 'error',
                               'message': "Не получается разобрать RSS канал. Может в URL ошиблись?", 'sort': 1})
                fields.sort(key=operator.itemgetter('sort'))

        # vkontakte
        if source == 'vk':
            pp = vkauth(request)
            if pp:
                s = Sync()
                s.source = pp
                s.user = pp.user
                s.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[s.id]))

            fields = [
                    #{'name': 'message', 'type': 'message', 'message': vk_notice},
                    {'name': 'vkauth', 'type': 'button', 'size': 5, 'value': 'Авторизация через сайт Vkontakte',
                     'onclick': 'vkontakteauth(\'%s%s?%s\');' % (HTTP_HOST, reverse('my.views.new'), 'src=vk')},
                    #{'name': 'token', 'type': 'text', 'size': 50, 'label': 'Token'},
                    #{'name': 'feedsave', 'type': 'submit', 'value': 'Далее'},
            ]

        # twitter
        if source == 'twitter':
            pp = twauth(request)
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
                    {'name': 'twauth', 'type': 'button', 'size': 5, 'value': 'Авторизоваться через Twitter',
                     'onclick': 'twitterauth(\'%s?src=twitter\', \'%s\');' % (
                         reverse('my.views.new'), register['url'])},
            ]

        #facebook
        if source == 'fb':
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


        # forsquare
        if source == 'fs':
            callbackurl = "%s%s%%3Fsrc%%3Dfs" % (HTTP_HOST, reverse('my.views.new'))
            pp = fsauth(request, callbackurl)
            if pp:
                s = Sync()
                s.source = pp
                s.user = pp.user
                s.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[s.id]))

            fields = [
                    {'name': 'fsauth', 'type': 'button', 'size': 5, 'value': 'Авторизация через сайт Foursquare',
                     'onclick': 'foursquareauth(\'%s\');' % callbackurl},
            ]


        #livejournal
        if source == 'lj':
            if request.POST:
                pp = PostPlace()
                pp.sn_type = SNType.objects.get(code='lj')
                pp.user = request.user
                pp.login = request.POST['user']
                pp.password = md5.md5(request.POST['password']).hexdigest()
                pp.save()
                s = Sync()
                s.source = pp
                s.user = pp.user
                s.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[s.id]))

            fields = [
                    {'name': 'message', 'type': 'message', 'message': lj_notice},
                    {'name': 'user', 'type': 'text', 'size': 50, 'label': 'Lj user'},
                    {'name': 'password', 'type': 'password', 'size': 50, 'label': 'Password'},
                    {'name': 'feedsave', 'type': 'submit', 'value': 'Продолжить'},
            ]

    return {'sn_types': sn_types, 'source': source, 'fields': fields}


def feedtest(request):
    response = None
    if 'url' not in request.GET and 'feedurl' not in request.POST:
        response = "No valid url"
    else:
        if 'url' in request.GET:
            url = request.GET['url']
        else:
            url = request.POST['feedurl']
        try:
            feed = feedparser.parse(url)
            if feed.status == 200:
                response = "Feed ok"
            else:
                response = "Feed status: %s" % feed.status
        except Exception:
            response = "Can't parse feed"
    return HttpResponse(response)


@login_required()
@render_to('my/sync.html')
def sync(request, syncid):
    errors = []
    try:
        sync = Sync.objects.get(pk=syncid)
    except Sync.DoesNotExist:
        return HttpResponseNotFound()
    sn_types = SNType.objects.filter(read_only=False)
    if request.POST:
        sync.title = request.POST['synctitle']
        sync.save()
        for var in request.POST.keys():
            test = re.findall("sync_target_id_(\d+)", var)
            if test and test[0] and request.POST[var]:
                pp = PostPlace.objects.get(pk=test[0])
                pp.userid = request.POST[var]
                pp.save()

        for var in request.POST.keys():
            test = re.findall("userid_(\d+)", var)
            if test and test[0] and request.POST[var]:
                pp = PostPlace.objects.get(pk=test[0])
                pp.userid = request.POST[var]
                pp.save()

    if sync.source.sn_type.code == 'vk':
        vk = VK(vk_settings)
        groups = vk.VKGetGroups(sync.source.access_token)
        if 'error' in groups:
            raise Exception, groups['error']['error_msg']

        if 'response' in groups:
            groups = groups['response']
            sync.source.sources = []
            for i in range(1, len(groups)):
                group = groups[i]
                if group['is_admin']:
                    sync.source.sources.append({'id': group['gid'], 'name': group['name']})

    if sync.source.sn_type.code == 'fb':
        fb_settings['redirect_uri'] = "%s%s?src=fb" % (HTTP_HOST, reverse('my.views.new'))
        fb = FB(fb_settings, code=sync.source.access_token)

        sync.source.sources = []

        try:
            fb.login()
            groups = fb.getGroups()
            pages = fb.getPages()
        except Exception:
            pass
        if groups:
            for group in groups:
                if 'administrator' in group:
                    sync.source.sources.append({'id': int(group['id']), 'name': 'Группа - ' + group['name']})

        if pages:
            for page in pages:
                sync.source.sources.append({'id': int(page['id']), 'name': 'Страницы - ' + page['name']})

#        for group in groups:
#            if 'administrator' in group:
#                sync.source.sources.append({'id': int(group['id']), 'name': group['name']})

    destination = None
    destinations_vk = []
    destinations_fb = []

    fields = None

    if 'destination' in request.GET:
        destination = request.GET['destination']

        if destination == 'vk':
            if request.POST and 'token' in request.POST:
                pp = PostPlace()
                pp.sn_type = SNType.objects.get(code='vk')
                pp.user = request.user
                pp.access_token = request.POST['token']
                pp.save()
                sync.destination.add(pp)
                sync.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[sync.id]))
            fields = [

                    {'name': 'vkauth', 'type': 'button', 'size': 5, 'value': 'Авторизация через сайт Vkontakte',
                     'onclick': 'vkontakteauth(\'%s%s\');' % (HTTP_HOST, reverse('my.views.syncvk', args=[sync.id]))},
            ]

        if destination == 'twitter':
            tw = Tweet(twitter_settings)
            register = tw.register(
                callbackurl="%s%s" % (HTTP_HOST, reverse('my.views.synctwitter', args=[sync.id])))
            request.session['oauth_token_secret'] = register['data']['oauth_token_secret']
            request.session['oauth_token'] = register['data']['oauth_token']
            fields = [
                    {'name': 'twauth', 'type': 'button', 'size': 5, 'value': 'Авторизоваться через Twitter',
                     'onclick': 'twitterauth(\'%s\', \'%s\');' % (
                         reverse('my.views.synctwitter', args=[sync.id]), register['url'])},
            ]

        if destination == 'fb':
            fb_settings['redirect_uri'] = "%s%s" % (HTTP_HOST, reverse('my.views.syncfacebook', args=[sync.id]))
            fb = FB(fb_settings)
            url = fb.register()

            fields = [
                    {'name': 'fbauth', 'type': 'button', 'size': 5, 'value': 'Авторизоваться через Facebook',
                     'onclick': 'facebookauth(\'%s\');' % url},
            ]

        #livejournal
        if destination == 'lj':
            if request.POST:
                pp = PostPlace()
                pp.sn_type = SNType.objects.get(code='lj')
                pp.user = request.user
                pp.login = request.POST['user']
                pp.password = md5.md5(request.POST['password']).hexdigest()
                pp.save()
                sync.destination.add(pp)
                sync.save()
                return HttpResponseRedirect(reverse('my.views.sync', args=[sync.id]))

            fields = [
                    {'name': 'message', 'type': 'message', 'message': lj_notice},
                    {'name': 'user', 'type': 'text', 'size': 50, 'label': 'Lj user'},
                    {'name': 'password', 'type': 'password', 'size': 50, 'label': 'Password'},
                    {'name': 'feedsave', 'type': 'submit', 'value': 'Продолжить'},
            ]


    if sync.destination.all():
        for dest in sync.destination.all():
            new_sn_types = []
            for sn_type in sn_types:
                if sn_type != dest.sn_type:
                    new_sn_types.append(sn_type)
            sn_types = new_sn_types
            if dest.sn_type.code == 'vk':
                req = "https://api.vkontakte.ru/method/groups.get?access_token=%s&extended=1" % dest.access_token
                resp = urllib2.urlopen(req)
                groups = json.loads(resp.read())
                if 'error' in groups:
                    errors.append({'dest_id': dest.id, 'message': groups['error']['error_msg']})
                    sync.destination.remove(dest)
                if 'response' in groups:
                    groups = groups['response']
                    for i in range(1, len(groups)):
                        group = groups[i]
                        if group['is_admin']:
                            destinations_vk.append({'id': group['gid'], 'name': group['name']})

            if dest.sn_type.code == 'fb':
                groups = None
                pages = None
                fb_settings['redirect_uri'] = "%s%s" % (HTTP_HOST, reverse('my.views.syncfacebook', args=[sync.id]))
                fb = FB(fb_settings, code=dest.access_token)
                try:
                    fb.login()
                    groups = fb.getGroups()
                    pages = fb.getPages()
                except Exception:
                    pass
                if groups:
                    for group in groups:
                        if 'administrator' in group:
                            destinations_fb.append({'id': int(group['id']), 'name': 'Группа - ' + group['name']})

                if pages:
                    for page in pages:
                        destinations_fb.append({'id': int(page['id']), 'name': 'Страница - ' + page['name']})

    return {'sync': sync, 'sn_types': sn_types, 'destination': destination, 'fields': fields,
            'destinations_vk': destinations_vk, 'destinations_fb': destinations_fb, 'errors': errors}


@login_required()
@render_to('my/syncvk.html')
def syncvk(request, syncid):
    if not request.user:
        return HttpResponseRedirect(reverse('registration.views.login'))
    sync = Sync.objects.get(pk=syncid)
    pp = vkauth(request)
    if pp:
        sync.destination.add(pp)
        sync.save()
        return HttpResponseRedirect(reverse('my.views.sync', args=[sync.id]))
    return {}


@login_required()
@render_to('my/syncvk.html')
def syncfoursqare(request, syncid):
    if not request.user:
        return HttpResponseRedirect(reverse('registration.views.login'))
    sync = Sync.objects.get(pk=syncid)
    pp = vkauth(request)
    if pp:
        sync.destination.add(pp)
        sync.save()
        return HttpResponseRedirect(reverse('my.views.sync', args=[sync.id]))
    return {}


def vkauth(request):
    if request.POST and 'token' in request.POST:
        pp = PostPlace()
        pp.sn_type = SNType.objects.get(code='vk')
        pp.access_token = request.POST['token']
        pp.user_id = 0
        pp.user = request.user
        pp.save()
        return pp

    if 'code' in request.GET:
        code = request.GET['code']
        vk = VK(vk_settings)
        jdata = vk.VKRegister(code)
        pp = PostPlace()
        pp.sn_type = SNType.objects.get(code='vk')
        pp.access_token = jdata['access_token']
        pp.user_id = jdata['user_id']
        pp.user = request.user
        pp.save()
        return pp
    else:
        return False


def fsauth(request, callbackurl):
    if 'code' in request.GET:
        code = request.GET['code']
        fs = FS(fs_settings)
        jdata = fs.FSRegister(code, callbackurl)
        if jdata:
            pp = PostPlace()
            pp.sn_type = SNType.objects.get(code='fs')
            pp.access_token = jdata['access_token']
            pp.user = request.user
            pp.save()
            return pp
    else:
        return False


@login_required()
@render_to('my/synctwitter.html')
def synctwitter(request, syncid):
    if not request.user:
        return HttpResponseRedirect(reverse('registration.views.login'))
    sync = Sync.objects.get(pk=syncid)
    pp = twauth(request)
    if pp:
        sync.destination.add(pp)
        sync.save()
        return HttpResponseRedirect(reverse('my.views.sync', args=[sync.id]))
    return {}


def twauth(request):
    if 'oauth_token' in request.GET and 'oauth_verifier' in request.GET:
        tw = Tweet(twitter_settings)
        reg = tw.register(oauth_token=request.session['oauth_token'],
                          oauth_secret=request.session['oauth_token_secret'],
                          pin=request.GET['oauth_verifier'])
        if not reg:
            raise Exception, reg
        if 'oauth_token_secret' in reg and 'oauth_token' in reg:
            pp = PostPlace()
            pp.userid = reg['user_id']
            pp.sn_type = SNType.objects.get(code='twitter')
            pp.access_token = reg['oauth_token']
            pp.access_token_secret = reg['oauth_token_secret']
            pp.user = request.user
            pp.save()
            return pp
    return False


@login_required()
@render_to('my/synctwitter.html')
def syncfacebook(request, syncid):
    if not request.user:
        return HttpResponseRedirect(reverse('registration.views.login'))
    sync = Sync.objects.get(pk=syncid)
    pp = fbauth(request)
    if pp:
        sync.destination.add(pp)
        sync.save()
        return HttpResponseRedirect(reverse('my.views.sync', args=[sync.id]))
    return {}


def fbauth(request):
    if 'code' in request.GET:
        pp = PostPlace()
        pp.sn_type = SNType.objects.get(code='fb')
        pp.access_token = request.GET['code']
        pp.user = request.user
        pp.save()
        return pp
    return False


@login_required()
@render_to('my/delsync.html')
def delsync(request, syncid):
    try:
        sync = Sync.objects.get(pk=syncid)
    except Sync.DoesNotExist:
        return HttpResponseNotFound()
    for dest in sync.destination.all():
        dest.delete()

    sync.source.delete()
    sync.delete()
    return HttpResponseRedirect(reverse('my.views.index'))


@login_required()
@render_to('my/profile.html')
def profile(request):
    #url, created = UserProfile.objects.get_or_create(user = request.user)
    return {'user': request.user}

@login_required()
def deldest(request, syncid, ppid):
    try:
        pp = PostPlace.objects.get(pk=ppid)
    except PostPlace.DoesNotExist:
        raise Exception, "Something wrong..."

    pp.delete()

    return redirect(reverse("my.views.sync", args=[syncid]))