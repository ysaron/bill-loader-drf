from django.contrib import admin
from .models import Bill, Client, Organization, Service


@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('organization', 'number', 'sum', 'date', 'fraud_score')
    list_filter = ('client', 'organization')
    search_fields = ('client', 'organization')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'client', 'fraud_weight')
    list_filter = ('client',)
    search_fields = ('client', 'address')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass
