import requests
import json
from munch import munchify
from retrying import retry
import datetime

IGNORE_PARAMS = ('uri', 'path')

class API_Basic:
    def __init__(self, key,
                 host_url,
                 api_version,
                 resource,
                 params=None, **kwargs):
        self.prefix_path = '/api/{}/{}'.format(api_version, resource)
        self.params = params
        self.host_url = host_url
    
    def get_tender(self, TenderID):
        r = requests.get('{}/{}/{}'.format(self.host_url, self.prefix_path, TenderID),params = self.params)
        return r.content
 
    def _update_params(self, params):
       for key in params:
           if key not in IGNORE_PARAMS:
               self.params[key] = params[key]
 
    #@retry(stop_max_attempt_number=5,)
    def get_tenders(self, params = {}, feed='changes'):
        DateTime = datetime.datetime.now()
        Date = DateTime.date()
        try:
            if self.params['offset'][0:10] != str(Date): 
                return ''
        except Exception:
            print('')
        #params['feed'] = feed
        try:
            self._update_params(params)
            r = requests.get('{}{}'.format(self.host_url, self.prefix_path),params = self.params)
            if r.status_code == 200:
                decoded_tender = json.loads(r.content)
                tender = munchify(decoded_tender['data'])
                self._update_params(decoded_tender['next_page'])
                return tender
        except ConnectionAbortedError:
            del self.params['offset']
            raise

        raise print(r.status_code)

  
  
class Client(API_Basic):
       def __init__(self, key,
                 host_url= "https://public.api.openprocurement.org",
                 api_version='2.5',
                 params={},
                 resource='tenders'):
        super(Client, self).__init__(key, host_url, api_version, resource, params)
        

