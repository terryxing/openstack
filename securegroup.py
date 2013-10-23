import novaclient.v1_1.client as nvclient
from credentials import get_nova_creds
import time
creds = get_nova_creds()
nova = nvclient.Client(**creds)

#print nova.security_groups.list()
#time.sleep(10)


secgroup = nova.security_groups.find(name="default")
nova.security_group_rules.create(secgroup.id,
                               ip_protocol="tcp",
                               from_port=22,
                               to_port=22)
nova.security_group_rules.create(secgroup.id,
                               ip_protocol="icmp",
                               from_port=-1,
                               to_port=-1)
nova.security_group_rules.create(secgroup.id,
                               ip_protocol="udp",
                               from_port=53,
                               to_port=53)
