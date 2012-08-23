#!/bin/bash

export PYTHONPATH="$PYTHONPATH:/var/www/html/dev.copy-post.ru/html"
export DJANGO_SETTINGS_MODULE="live_settings"
python /var/www/html/dev.copy-post.ru/html/sync.py -s $1  &  >> /tmp/log 2>&1