# -*- coding: utf-8 -*-
VERSION = (0, 1, 0)
__version__ = '.'.join(map(str, VERSION))

from django.utils.functional import LazyObject


class WatershedService(LazyObject):
    def _setup(self):
        from django.conf import settings
        from django.utils.importlib import import_module
        module, cls = getattr(
            settings, 'USTREAM_WATERSHED_SERVICE',
            'ustream_watershed.service.BaseWatershedService').rsplit('.', 1)
        self._wrapped = getattr(import_module(module), cls)()


watershed_service = WatershedService()
