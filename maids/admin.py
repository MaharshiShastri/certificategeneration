from django.contrib import admin
from customer.models import CustomUser as cust
from maids.models import CustomUser
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(cust)