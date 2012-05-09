# -*- coding: utf-8 -*-
from django.http import HttpResponse


class SoapView(object):
    """ Django Soap View
        @see pysimplesoap.server.SOAPHandler
    """
    def __init__(self, service):
        self.service = service

    def __call__(self, request):
        response = HttpResponse(content_type='text/xml')
        url = self._get_absolute_path(request)
        self.service.dispatcher.location = url
        self.service.dispatcher.action = url
        response.content = getattr(self, 'do_%s' % request.method)(request)
        return response

    def do_GET(self, request):
        # XXX: only wsdl response
        # TODO: SOAP response
        return self.service.dispatcher.wsdl()

    def do_POST(self, request):
        return self.service.dispatcher.dispatch(request.raw_post_data)

    def _get_absolute_path(self, request):
        return u'http%s://%s%s' % (
            request.is_secure() and 's' or '',
            request.get_host(), request.path)
