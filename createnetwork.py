import os
from sys import argv
import random
import logging
from quantumclient.v2_0 import client
#logging.basicConfig(level=logging.DEBUG)

def createnetwork():
    quantum = client.Client(username='admin', password='admin', tenant_name='admin', auth_url=os.environ['OS_AUTH_URL'])
    quantum.format= 'json'
    netname = str(argv[1])

    print netname


    if quantum.list_networks(name=netname)['networks']:
        print "existing network ID:",  quantum.list_networks(name=netname)["networks"][0]["id"]
        print "network name exists... generating a random name for that"
        
        netname = netname + str(random.randrange(1,100))
    
    network = {'name': netname, 'admin_state_up': True}
    nets = quantum.create_network({'network':network})

    print 'network:'+ netname  + ' is created' 

    id = nets['network']['id']


    cidr = str(argv[2])
    
    allocationpool = [{'start': '172.16.0.10', 'end': '172.16.0.100'}]
#    subnets = {'network_id':id, 'ip_version':4, 'cidr': cidr, 'allocation_pools':allocationpool}


    subnets = {'network_id':id, 'ip_version':4, 'cidr': cidr}
    quantum.create_subnet({'subnet': subnets})

    print "subnet: ", subnets['cidr'], " is created for network:", netname

#print "deleting the network"
#quantum.delete_network(nets['networks'][0]['id'])


if __name__ == "__main__":
     
    if len(argv)!=3:
        print 'this script takes exactly two arguments, usages:  ./createnetwork.py  networkname cidr'
        exit()
    else:
        createnetwork()
