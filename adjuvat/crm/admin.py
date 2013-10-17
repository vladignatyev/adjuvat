from crm.models import Order, PricingItem, Executor, Service, Client, Company
from django.contrib import admin

__author__ = 'ignatev'

admin.site.register(Company)
admin.site.register(Client)
admin.site.register(Service)
admin.site.register(Executor)
admin.site.register(PricingItem)
admin.site.register(Order)