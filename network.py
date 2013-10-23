import keystoneclient.v2_0.client as ksclient
import logging
from neutronclient.neutron import client
endpoint="http://192.168.1.111:9696/v2.0"
admin_token = "123456"
logging.basicConfig(level=logging.DEBUG)
neutron = client.Client('2.0', endpoint=endpoint, token=admin_token)
#neutron.format = 'json'
network = {'name': 'mynetwork', 'admin_state_up': True}
neutron.create_network({'network':network})
#keystone = ksclient.Client(endpoint='192.168.1.111:5000/v2.0', token=admin_token)
print neutron
#neutron.create_network({'network':network})
