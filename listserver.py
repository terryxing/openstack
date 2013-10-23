import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds
creds = get_nova_creds()
nova = nvclient.Client(**creds)
print nova.servers.list()

server = nova.servers.find(name="instance2")
server.reboot()

