from customer.models import Client

# create your public tenant
tenant = Client(domain_url='hicsistema.herokuapp.com/', # don't add your port or www here! on a local server you'll want to use localhost here
                schema_name='public',
                name='Sucursal1',
                plan='ANUAL',
                started_date='2020-12-12'
               )
tenant.save()