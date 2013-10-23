import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds
import time

creds = get_nova_creds()
nova = nvclient.Client(**creds)

instance = nova.servers.find(name="pyapiinstance2")

if instance.status == 'ACTIVE':
    instance.suspend()
    print "start suspending"
    status = instance.status
    while status != 'SUSPENDED':
        time.sleep(5)
        instance = nova.servers.get(instance.id)
        status = instance.status
    print "the current status is ", instance.status
elif instance.status == 'SUSPENDED':
    print "the status is already suspended"
else:
    print "wrong status, exiting..."
    exit(0)

print "sleep for 30 seconds for checking if the instance is really suspended from horizon"
time.sleep(30)

if instance.status == 'SUSPENDED':
    instance.resume()
    print"start resuming.."
    status = instance.status
    while status != 'ACTIVE':
        time.sleep(5)
        instance = nova.servers.get(instance.id)
        status = instance.status   
print "the current status is", instance.status
