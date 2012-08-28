#!/usr/bin/env python
# -*- coding: utf-8 -*-
#export PYTHONPATH=$PYTHONPATH:c:/work/copypost

import os, re, time, datetime
from optparse import OptionParser
from django.conf import settings
from tweet import Tweet
from django.core.urlresolvers import reverse
from fb import FB
from vk import VK
from ljapi import LJPost
import random
from stripogram import html2text, html2safehtml
import json

os.environ['DJANGO_SETTINGS_MODULE'] = 'live_settings'
from live_settings import *

parser = OptionParser()
parser.add_option("-s", "--sync", dest="syncid")
parser.add_option("-d", "--debug", dest="debug", action="store_true")
(options, args) = parser.parse_args()
import feedparser, urllib, urllib2
from urllib import quote

MAX_POST_ITEMS = 14

if options.debug:
    DEBUG = True

if not options.syncid:
    raise Exception, 'Nothing to do'

from my.models import Sync, PostItem, PostPlace

try:
    sync = Sync.objects.get(pk=options.syncid)
    sync.updating = True
    sync.save()
except Sync.DoesNotExist:
    raise Exception, "Sync with id=%s does not exists" % options.syncid

source = sync.source
messages = []
img_ext = ('jpg', 'gif', 'JPG', 'jpeg', 'JPEG', 'GIF', 'png', 'PNG')


#Source - RSS
if source.sn_type.code == 'rss':
    feed = feedparser.parse(source.url)
    if hasattr(feed, 'status') and feed.status == 200:
        items = feed.items()[8][1]
        max_items = MAX_POST_ITEMS
        if len(items) < MAX_POST_ITEMS:
            max_items = len(items)
        for i in range(0, max_items):
            error = 0
            source_message = {'text': '', 'attachements': []}
            try:
                item = items[i]
            except Exception:
                item = items

            try:
                if 'guid' in item:
                    exist = PostItem.objects.get(pk=item['guid'])
                    error = 1
                    sync.updating = False
                    sync.save()
                else:
                    if 'link' in item:
                        item['guid'] = item['link']
                        exist = PostItem.objects.get(pk=item['link'])
                    else:
                        error = 1
                        sync.updating = False
                        sync.save()

            except PostItem.DoesNotExist:
                if (not error):
                    pi = PostItem()
                    pi.guid = item['guid']
                    if 'description' in item:
                        pi.message = item['description']
                    else:
                        pi.message = item['title']
                    pi.title = item['title']
                    pi.pp = source
                    pi.save()
                    source_message['guid'] = pi.guid
                    source_message['text'] = pi.message
                    source_message['title'] = pi.title
                    source_message['attachements'].append({"type": "url", "src": item['link']})
                    if 'summary' in item:
                        for ext in img_ext:
                            if item['summary'].find(ext) != -1:
                                match = re.findall(r"src=[\'\"](.*?)[\"\']", item['summary'])
                                if match[0]:
                                    source_message['attachements'].append({"type": "img", "src": match[0]})

                    messages.append(source_message)

# Source - vk
if source.sn_type.code == 'vk':
    vk = VK(vk_settings)
    posts = vk.VKGetWall(source, MAX_POST_ITEMS)
    if 'response' in posts:
        posts = posts['response']
        for i in range(1, len(posts)):
            source_message = {'text': '', 'attachements': []}
            guid = "%s%s%s" % (posts[i]['id'], posts[i]['from_id'], posts[i]['to_id'])
            try:
                exist = PostItem.objects.get(pk=guid)
                sync.updating = False
                sync.save()
            except PostItem.DoesNotExist:
                pi = PostItem()
                pi.pp = source
                pi.message = posts[i]['text']
                pi.guid = guid
                try:
                    pi.save()
                except Exception:
                    pass

                if 'text' in posts[i]:
                    try:
                        source_message['text'] = posts[i]['text']
                    except Exception:
                        source_message['text'] = ""
                if 'attachments' in posts[i]:
                    for attach in posts[i]['attachments']:
                        if 'photo' in attach:
                            source_message['attachements'].append({"type": "photo", "src": attach['photo']['src_big']})
                        if 'link' in attach:
                            source_message['attachements'].append({"type": "url", "src": attach['link']['url']})
                messages.append(source_message)


# Source - fb
if source.sn_type.code == 'fb':
    fb_settings['redirect_uri'] = "%s%s?src=fb" % (HTTP_HOST, reverse('my.views.new'))
    fb = FB(fb_settings, code=source.access_token)
    fb.login()
    try:
        posts = fb.getGroupFeed(source.userid)
    except Exception:
        posts = []
    max_items = MAX_POST_ITEMS
    if len(posts) < MAX_POST_ITEMS:
        max_items = len(posts)
    for i in range(0, max_items):
        source_message = {'text': '', 'attachements': []}
        item = posts[i]
        try:
            exist = PostItem.objects.get(pk=item['id'])
        except PostItem.DoesNotExist:
            pi = PostItem()
            pi.pp = source
            pi.message = item['message']
            pi.guid = item['id']
            pi.save()

            source_message['text'] = item['message']
            if 'picture' in item:
                source_message['attachements'].append({"type": "photo", "src": item['picture']})
            messages.append(source_message)

print messages

for item in messages:
    for destination in sync.destination.all():
        print destination.sn_type
        if destination.sn_type.code == 'vk' and destination.enabled:
            vk = VK(vk_settings)
            attachments = []
            message = ""
            if item['text']:
                message = "%s" % (item['title']) #, html2safehtml(item['text'])
            if item['attachements']:
                for attach in item['attachements']:
                    attachments.append(attach['src'])
            if message:
                res = vk.VKPost(destination, message, attachments)
                try:
                    js = json.loads(res)
                    if 'error' in js:
                        raise Exception, 'error found in vk responce'
                    else:
                        print res
                except Exception:
                    destination.enabled = False
                    destination.save()


        if destination.sn_type.code == 'twitter':
            message = ""
            tw = Tweet(twitter_settings)
            tw.login(destination.access_token, destination.access_token_secret)
            if item['title']:
                message = "%s" % item['title']
            if item['attachements']:
                for attach in item['attachements']:
                    message += " %s" % attach['src']
            if message:
                if tw.post(message):
                    print 'Twitter fucked'

        if destination.sn_type.code == 'fb':
            fb_settings['redirect_uri'] = "%s%s" % (HTTP_HOST, reverse('my.views.syncfacebook', args=[sync.id]))
            fb = FB(fb_settings, code=destination.access_token)
            fb.login()
            message = ""
            text = ""
            if 'title' in item:
                message = "%s" % (item['title'])
            if 'text' in item:
                text = html2safehtml(item['text'])
            if text:
                message += " - " + text
            if 'attachements' in item:
                for attach in item['attachements']:
                    message += " %s" % attach['src']
            if message:
                message = message.encode('utf-8')
                if destination.userid:
                    profile = destination.userid
                else:
                    profile = "me"
                fb.wallPost(message=message, profile_id=str(profile))
            print 'Facebook fucked'

        if destination.sn_type.code == 'lj':
            try:
        	LJPost(destination, item)
                print 'LJ fucked'
            except Exception:
                print 'LJ not fucked'

        if destination.sn_type.code == 'free':
            req = destination.url
            data = {
                'token': destination.access_token,
                'message': "%s - %s\nИсточник: %s" % (
                item['title'].encode('utf-8'), item['text'].encode('utf-8'), item['guid'].encode('utf-8'))
            }
            print req, data
            resp = urllib2.urlopen(req, urllib.urlencode(data))
            params = resp.read()
            print params
        time.sleep(random.randrange(10, 60))

sync.last_sync = datetime.datetime.now()
sync.updating = False
sync.save()
