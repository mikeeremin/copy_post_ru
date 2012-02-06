# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from registration.forms import RegistrationFormUniqueEmail

admin.autodiscover()

urlpatterns = patterns('', url(r'^admin/', include(admin.site.urls)),
    (r'^$', 'views.index'),
    (r'^about/$', 'views.about'),
    (r'^my/', include('my.urls')),


    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
         {'document_root': 'media',
          'show_indexes': True}),
                       url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
                               {'next_page': '/', 'template_name': ''}),
                       #(r'^accounts/', include('invitation.urls')),
    (r'^accounts/', include('registration.urls')),
                       url(r'^accounts/register/$', 'registration.views.register',
                               {'form_class': RegistrationFormUniqueEmail}, name='registration_register'),
    (r'^news/', include('news.urls')),
    (r'^faq/', include('faq.urls')),
                       )
