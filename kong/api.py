class API:

    _valid_attributes = {'created_at', 'hosts', 'http_if_terminated',
                         'https_only', 'id', 'name', 'preserve_host',
                         'retries', 'strip_uri', 'upstream_connect_timeout',
                         'upstream_read_timeout', 'upstream_send_timeout',
                         'upstream_url', 'request_path', 'request_host'}

    _exclude_difference = {'created_at', 'id'}

    NEW_STATE = 0
    CREATED_STATE = 1
    DELETED_STATE = 2

    def __init__(self, is_new=True, **kwargs):
        self.attributes = {}
        self._populate_attributes(**kwargs)
        self._state = API.NEW_STATE if is_new else API.CREATED_STATE

    def difference(self, other_api):
        for attribute in self._valid_attributes:
            if attribute not in self._exclude_difference and self.attributes.get(attribute) != other_api.attributes.get(attribute):
                return True
        return False

    def _populate_attributes(self, **attributes):
        for attribute in attributes:
            if attribute in self._valid_attributes:
                self.attributes[attribute] = attributes[attribute]

    def update_attributes(self, **attributes):
        self._state = API.CREATED_STATE
        self._populate_attributes(**attributes)

    def commit(self, kong_connection):
        if self._state == API.CREATED_STATE:
            return kong_connection.update_api(self)
        else:
            return kong_connection.create_api(self)

    def delete(self, kong_connection):
        if self._state != API.DELETED_STATE and self._state == API.CREATED_STATE:
            kong_connection.delete_api(self)
            self._state = API.DELETED_STATE


def create_api(**attributes):
    return API(**attributes)