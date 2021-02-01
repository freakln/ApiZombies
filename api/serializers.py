from django.contrib.auth.models import User, Group
from .models import Survivor, Inventory, Location, ReportInfect
from rest_framework import serializers
from collections import OrderedDict


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('water', 'food', 'medication', 'ammunition')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'latitude', 'longitude')


class SurvivorBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = ('id', 'name')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportInfect
        fields = ('survivor', 'motive')


class TradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('survivor', 'motive')


class SurvivorListSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many=False)
    location = LocationSerializer(many=False)

    class Meta:
        model = Survivor
        fields = ('name', 'gender', 'age', 'isInfected', 'inventory', 'location')


class SurvivorSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many=False)
    location = LocationSerializer(many=False)

    class Meta:
        model = Survivor
        fields = ('name', 'gender', 'age', 'inventory', 'location')

    def create(self, validated_data):
        print(validated_data)
        survivor_data = OrderedDict()
        survivor_fields = ['name', 'gender', 'age']

        for data in survivor_fields:
            survivor_data[data] = validated_data[data]

        inventors_data = validated_data.pop('inventory')
        locations_data = validated_data.pop('location')
        print(inventors_data)

        print(locations_data)

        survivor = Survivor.objects.create(**survivor_data)
        Inventory.objects.create(survivor=survivor, **inventors_data)
        Location.objects.create(survivor=survivor, **locations_data)
        return survivor
