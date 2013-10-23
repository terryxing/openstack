import keystoneclient.v2_0.client as ksclient
from credentials import get_keystone_creds

creds = get_keystone_creds() # See <a href="openrc-creds" />
keystone = ksclient.Client(**creds)
glance_endpoint = keystone.service_catalog.url_for(service_type='image',
                                                       endpoint_type='publicURL')
network_endpoint = keystone.service_catalog.url_for(service_type='network',
                                                       endpoint_type='publicURL')
compute_endpoint = keystone.service_catalog.url_for(service_type='compute',
                                                       endpoint_type='publicURL')
#neutron_endpoint = keystone.service_catalog.url_for(service_type='neutron',
#                                                       endpoint_type='publicURL')
print "glance endpoint is : " + glance_endpoint
print "network endpoint is : " + network_endpoint
print "compute endpoint is : " +  compute_endpoint
#print "neutron endpoint is : " +  neutron_endpoint
