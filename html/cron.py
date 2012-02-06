#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings, time
setup_environ(settings)
from settings import *
import datetime, os
from my.models import Sync
from django.db.models import Q

nextupdate = datetime.datetime.now() - datetime.timedelta(minutes=30)
try:
    sites = Sync.objects.filter(Q(last_sync__lte=nextupdate, updating=0)|Q(last_sync=None, updating=0))
    for site in sites:
        cmd = '%s %s &  >> /tmp/log 2>&1 ' % (SYNC_BIN, site.id)
        print cmd
        os.system( cmd )
        time.sleep(10)
except Sync.DoesNotExist:
    pass

