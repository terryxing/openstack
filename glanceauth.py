import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient
from credentials import get_keystone_creds
creds = get_keystone_creds()
keystone = ksclient.Client(**creds)
glance_endpoint = keystone.service_catalog.url_for(service_type='image',
                                                   endpoint_type='publicURL')
glance = glclient.Client(glance_endpoint, token=keystone.auth_token)
