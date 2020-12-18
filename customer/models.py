from django.db import models
from tenant_schemas.models import TenantMixin


class Client(TenantMixin):
    FREQUENCIES = (
        ('MENSUAL', "Mensual"),
        ('ANUAL', "Anual"),
    )
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    auto_create_schema = True
    started_date = models.DateField()
    plan = models.CharField(max_length=250)
    frequency = models.CharField(max_length=50, choices=FREQUENCIES, default="MENSUAL")
    last_payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name
