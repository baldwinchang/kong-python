from kong.api import create_api
from kong.connection import KongConnection


KONG_ADMIN_URL = ''

api_definitions = []

apis = {}

connection = KongConnection(KONG_ADMIN_URL)
connection.sync_apis(apis)