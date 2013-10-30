import os
from sys import argv
import random
import logging
from quantumclient.v2_0 import client

def createrouter():
    """ thus function will first check the arguments and check their id, finally create the router
        finally, create the router, add interface absed on the interfeace
    """
 
    # authenticate the nuetron client 

    quantum = client.Client(username='admin', password='admin', 
                            tenant_name='admin', 
                            auth_url=os.environ['OS_AUTH_URL'])
    quantum.format= 'json'


    # check if the router name exists or not

    routername = str(argv[1])
    if quantum.list_routers(name=routername)['routers']:
        print "existing router ID:",  quantum.list_routers(name=routername)["routers"][0]["id"]
        print "router name exists... generating a random name for that"
        routername = routername + str(random.randrange(1,100))
        print "newly generated routername is :", routername

    else:
        print "router new is okay to be used  !!!  router is about to be created... " 


    # get the uuid of external network

#    if quantum.list_networks(name='public')['networks']:
#        print "public network exists"
#        publicnetid = quantum.list_networks(name='public')['networks'][0]['id']
#        print "public network id is : ",  publicnetid
#    else:
#        print 'public network does not exist, exiting .....'
#        exit(0) 

    
    # get the uuid of the subnet by cidr (e.g.,172.16.0.0/24)
    
    subnetids = []
    for subnetcidr in argv[2:]:
        print "subnetcidr list is : ", subnetcidr
      
        if quantum.list_subnets(cidr=subnetcidr)['subnets']:
            subnetid = quantum.list_subnets(cidr=subnetcidr)['subnets'][0]['id']
            print 'the subnet ID is:', subnetid
            subnetids.append(subnetid)
        else:
            print 'the subnet does not exist, please check using "quantum subnet-list"'
   
 
    # create router with info above
    
    routers = {'name': routername, 'admin_state_up': True}
    router = quantum.create_router({'router':routers})

    print 'router:'+ routername  + ' is created' 

    routerid = router['router']['id']
    print 'router id is:', routerid


    # add subnets interfaces to the routers
    
    for subnetid in subnetids:
        subnet_id = {"subnet_id": subnetid }
        quantum.add_interface_router(routerid, body=subnet_id)


if False:

    # add public interface to the router

    subnetinfo = {'subnet_id': subnetid}
    quantum.add_interface_router(ubnetinfo)


if False:
    print "deleting the router"
    quantum.delete_router(router['routers'][0]['id'])


if __name__ == "__main__":

    if len(argv)<3:
         print "This function takes at least  two arguments, usage: ./createrouter.py routername  *subnet_cidr"
         exit(0) 
    else:
        print 'valid input ! '
        createrouter()
