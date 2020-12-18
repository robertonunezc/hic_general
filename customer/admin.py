from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Register your models here.
from customer.models import Client


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on', 'started_date', 'plan', 'frequency', 'last_payment_date', 'payment_amount')

admin.site.register(Client, ClientAdmin)

# admin.site.unregister(User)
# admin.site.unregister(Group)
