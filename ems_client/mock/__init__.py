"""
EMS API mock data class
"""
import json
from logging import getLogger
from hashlib import md5
import os.path


class EMSMockData(object):
    def __init__(self):
        self._log = getLogger('ems_client')

    def mock(self, port_name, method_name, params):
        try:
            fn = self.mock_file_path(port_name, method_name, params)
            self._log.debug("mock data: %s" % fn)
            mock_data_file = open(fn, 'r')
            mock_data = mock_data_file.read()
            mock_data_file.close()
            return mock_data
        except Exception as ex:
            self._log.exception(ex)
            return ''

    def mock_file_path(self, port_name, method_name, params):
        cwd = os.path.dirname(os.path.realpath(__file__))
        mock_data_filename = md5(self._normalize(params)).hexdigest().upper()
        return os.path.join(cwd, 'data', port_name, method_name,
                            mock_data_filename)

    @staticmethod
    def _normalize(params):
        ignored = ['auth']
        normalized = {}

        for k in params.keys():
            if k not in ignored:
                normalized[k] = params[k]

        return json.dumps(normalized, sort_keys=True).encode('ascii', 'ignore')
