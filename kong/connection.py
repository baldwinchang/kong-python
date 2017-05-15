import requests

from kong.api import API


class Connection:

    def __init__(self, url='http://localhost:8001'):
        self.url = url

    def _get(self, path='', **request_args):
        return requests.get(self.url + path, **request_args)

    def _post(self, path='', **request_args):
        return requests.post(self.url + path, **request_args)

    def _patch(self, path='', **request_args):
        return requests.patch(self.url + path, **request_args)

    def _delete(self, path='', **request_args):
        return requests.delete(self.url + path, **request_args)


class KongConnection(Connection):

    def _get_apis(self, response):
        data = response.get('data', [])
        return [self._get_api(**attributes) for attributes in data]

    def get_apis(self):
        response = self._get('/apis').json()
        return self._get_apis(response)

    def _get_api(self, **attributes):
        return API(is_new=False, **attributes)

    def get_api(self, id=''):
        attributes = self._get('/apis/' + id).json()
        return self._get_api(**attributes)

    def create_api(self, api):
        response = self._post('/apis', json=api.attributes).json()
        print(response, api.attributes)
        api.update_attributes(**response)
        return api

    def update_api(self, api):
        print('will update')
        response = self._patch('/apis/' + api.attributes.get('id', ''), json=api.attributes).json()
        print(response)
        api.update_attributes(**response)
        return api

    def delete_api(self, api):
        self._delete('/apis/' + api.attributes.get('id', ''))

    def sync_apis(self, apis):
        online_apis = {api.attributes.get('name'): api for api in self.get_apis()}
        for api in online_apis:
            if api in apis:
                # only update if there is a change in attributes
                if online_apis[api].difference(apis[api]):
                    online_apis[api].update_attributes(**apis[api].attributes)
                    online_apis[api].commit(self)

                # flag that we do not want to create this
                del apis[api]
            else:
                online_apis[api].delete(self)

        for api in apis:
            print(api, apis[api].attributes)
            apis[api].commit(self)


