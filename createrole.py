import keystoneclient.v2_0.client as ksclient
# Replace the method arguments with the ones from your local config
keystone = ksclient.Client(auth_url="http://192.168.1.111:5000/v2.0",
                           username="admin",
                           password="supersecret",
                           tenant_name="demo")

# Replace the values below with the ones from your local config
#endpoint = "http://192.168.1.111:5000/v2.0"
#admin_token = "123456"

#keystone = ksclient.Client(endpoint=endpoint, token=admin_token)



glance_service = keystone.services.create(name="glance",
                            service_type="image",
                            description="OpenStack Image Service")


print keystone.services.list()
#print keystone
#print glance_service
