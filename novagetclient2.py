import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds
'''
another way to import version, directly
'''
creds = get_nova_creds()
nova = nvclient.Client(**creds)

for key, value in creds.iteritems():
    print key, value

