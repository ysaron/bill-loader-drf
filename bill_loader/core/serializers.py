from rest_framework import serializers

from .models import Bill, Client, Organization, Service


class ClientSerializer(serializers.ModelSerializer):
    org_num = serializers.SerializerMethodField()
    income = serializers.SerializerMethodField()

    class Meta:
        model = Client
        fields = ('name', 'org_num', 'income')

    def get_org_num(self, obj):
        return obj.orgs.count()

    def get_income(self, obj):
        return obj.income


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = ('name', 'address', 'fraud_weight')


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ('cls', 'name')


class BillSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(slug_field='name', read_only=True)
    organization = OrganizationSerializer()
    service = ServiceSerializer()

    class Meta:
        model = Bill
        fields = '__all__'
