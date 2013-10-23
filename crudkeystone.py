import keystoneclient.v2_0.client as ksclient
endpoint = "http://192.168.1.111:5000/v2.0"
admin_token = "supersecret"

keystone = ksclient.Client(endpoint=endpoint, token=admin_token)
user_role = keystone.roles.create("user")
admin_role = keystone.roles.create("admin")
acme_tenant = keystone.tenants.create(tenant_name="Acme",
                        description="Employees of Acme Corp.",
                        enabled=True)
admin_user = keystone.users.create(name="admin",
                password="a.G'03134!j",
                email="cloudmaster@example.com", tenant_id=acme_tenant.id)
keystone.roles.add_user_role(admin_user, admin_role, acme_tenant)
