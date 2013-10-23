from novaclient import client as novaclient
from credentials import get_nova_creds
creds = get_nova_creds()
nova = novaclient.Client("1.1", **creds)


for key, value in creds.iteritems():
    print key, value

#print "username is :" ,   creds['username']; 
#print "password is : ",  creds['password']; 
#print "authentication url is :",   creds['auth_url'] ;
#print "tenant name is : ",  creds['tenant_name'] ;

print nova
