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

    quantum = client.Client(username='admin', password='admin',  tenant_name='admin', auth_url=os.environ['OS_AUTH_URL'])
    quantum.format= 'json'


    
    # check if the router name exists or not

    routername = str(argv[1])

    if quantum.list_routers(name=routername)['routers']:
        routerid =  quantum.list_routers(name=routername)["routers"][0]["id"]
    else:
        print "router does not exist. " 


    
    publicnetname = str(argv[2])
    publicnetid = quantum.list_networks(name=publicnetname)['networks'][0]['id']
    print "public net id is", publicnetid


#    cidr = str(argv[2])

#    subnetid = quantum.list_subnets(cidr=cidr)['subnets'][0]['id']

#    subnet_id = {'subnet_id': subnetid}

#    quantum.add_interface_router(routerid, body=subnet_id)


   # externalgw = {'external_gateway_info': {'network_id': publicnetid }}
    externalgw = {'network_id': publicnetid }
    quantum.add_gateway_router(routerid, body=externalgw)


if False:
   
    # create router with info above
    
    routers = {'name': routername, 'admin_state_up': True}
    router = quantum.create_router({'router':routers})

    print 'router:'+ routername  + ' is created' 

    routerid = router['router']['id']
    print 'router id is:', routerid


    # add subnets interfaces to the routers
    
    for subnetid in subnetids:
        subnet_id = {"subnet_id": subnetid }
        quantum.add_interface_router(subnet_id)


    # add public interface to the router

    subnetinfo = {'subnet_id': subnetid}
    quantum.add_interface_router(ubnetinfo)


if False:
    print "deleting the router"
    quantum.delete_router(router['routers'][0]['id'])


if __name__ == "__main__":

    if len(argv)!=3:
         print "This function takes at 1  arguments, usage: ./router_add_gateway.py routername publicnetname"
         exit(0) 
    else:
        print 'valid input ! '
        createrouter()
