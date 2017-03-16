"""
Base module to support exposing EMS SOAP Service methods
"""
from importlib import import_module
from django.conf import settings
from logging import getLogger
from suds.client import Client
from suds import WebFault
from suds.cache import ObjectCache
from ems_client.mock import EMSMockData
import sys
import os


def load_object_by_name(object_name):
    """Load an object from a module by name"""
    mod_name, attr = object_name.rsplit('.', 1)
    mod = import_module(mod_name)
    return getattr(mod, attr)


class EMSAPIException(Exception):
    pass


class EMSAPI(object):
    """EMS API base
    """

    def __init__(self, options={}):
        self._log = getLogger('ems_client')
        cache_path = "/tmp/{0}-suds".format(os.getuid())
        client_opts = {'cache': ObjectCache(cache_path, days=1)}
        if hasattr(settings, 'EMS_API_TRANSPORT_CLASS'):
            transport = load_object_by_name(settings.EMS_API_TRANSPORT_CLASS)
            client_opts['transport'] = transport()
            client_opts['location'] = '%s/EMSAPI/Service.asmx' % (
                settings.EMS_API_HOST)
        self._api = Client(options.get('wsdl'), **client_opts)
        self._api.set_options(cachingpolicy=0)

        if not getattr(settings, 'EMS_API_HOST', False):
            self._data = self._mock
        else:
            self._data = self._live

    def _request(self, methodName, params={}):
        return self._data(methodName, params)
        try:
            pass
        except WebFault as err:
            self._log.exception(err)
            raise EMSAPIException(err)
        except Exception as err:
            self._log.error('Error: ' + str(sys.exc_info()[1]))
            raise EMSAPIException('Other error: ' + str(sys.exc_info()[1]))

    def _live(self, methodName, params={}):
        params['UserName'] = settings.EMS_API_USERNAME
        params['Password'] = settings.EMS_API_PASSWORD
        return self._api.service[self._port][methodName](**params)

    def _mock(self, methodName, params={}):
        reply = EMSMockData().mock(self._port, methodName, params)
        return self._api.service[self._port][methodName](
            __inject={'reply': reply})
