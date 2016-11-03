"""
Base module to support exposing EMS SOAP Service methods
"""
from django.conf import settings
from logging import getLogger
from suds.client import Client
from suds import WebFault
from suds.cache import ObjectCache
from ems_client.mock import EMSMockData
import sys
import os


class EMSAPIException(Exception):
    pass


class EMSAPI(object):
    """EMS API base
    """

    def __init__(self, options={}):
        self._log = getLogger('ems_client')
        cache_path = "/tmp/{0}-suds".format(os.getuid())
        cache = ObjectCache(cache_path, days=1)
        self._api = Client(options.get('wsdl'), cache=cache)
        self._api.set_options(cachingpolicy=0)

        if getattr(settings, 'EMS_API_MOCKDATA', False):
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
