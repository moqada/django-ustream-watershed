# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns
from django.conf.urls.defaults import url
from ustream_watershed.views import SoapView
from ustream_watershed import watershed_service


urlpatterns = patterns(
    '',
    url(r'^soap/$', SoapView(watershed_service), name='ustream_watershed-soap'),
    )
