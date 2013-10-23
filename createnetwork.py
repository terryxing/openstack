import os
from sys import argv
import random
import logging
from neutronclient.v2_0 import client
#logging.basicConfig(level=logging.DEBUG)

def createnetwork():
    neutron = client.Client(username='admin', password='supersecret', tenant_name='demo', auth_url=os.environ['OS_AUTH_URL'])
    neutron.format= 'json'
    netname = str(argv[1])

    print netname

   # print neutron.list_networks(name=netname)

   # print neutron.list_networks(name=netname)["networks"][0]["id"]

    if neutron.list_networks(name=netname)['networks']:
        print "existing network ID:",  neutron.list_networks(name=netname)["networks"][0]["id"]
        print "network name exists... generating a random name for that"
        
        netname = netname + str(random.randrange(1,100))
    
    network = {'name': netname, 'admin_state_up': True}
    nets = neutron.create_network({'network':network})

    print 'network:'+ netname  + ' is created' 

    id = nets['network']['id']


    #allocationpool = {'start': '172.16.0.10', 'end': '172.16.0.100'}
    #subnets = {'network_id':'91249d38-a261-4482-be5a-a79397dbdffb', 'ip_version':4, 'cidr': '172.16.0.0/24', 'allocation_pools':allocationpool}

    subnets = {'network_id':id, 'ip_version':4, 'cidr': '172.16.0.0/24'}
    neutron.create_subnet({'subnet': subnets})

    print "subnet: ", subnets['cidr'], " is created for network:", netname

#print "deleting the network"
#neutron.delete_network(nets['networks'][0]['id'])


if __name__ == "__main__":
    createnetwork()
