from django_filters import rest_framework as filters

from ..models import Bill, Client, Organization


class BillFilter(filters.FilterSet):
    client = filters.ModelChoiceFilter(
        queryset=Client.objects.all(),
        field_name='client',
        to_field_name='name',
    )
    organization = filters.ModelChoiceFilter(
        queryset=Organization.objects.all(),
        field_name='organization',
        to_field_name='name',
    )

    class Meta:
        model = Bill
        fields = ('client', 'organization')
