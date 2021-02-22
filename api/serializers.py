from django.contrib.auth.models import User, Group


from .models import Survivor, Inventory, Location, ReportInfect, Trade
from rest_framework import serializers
from collections import OrderedDict

values = {'water': 4,
          'food': 3,
          'medication': 2,
          'ammunition': 1}


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
        fields = ('latitude', 'longitude')


class SurvivorBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Survivor
        fields = ('id', 'name')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportInfect
        fields = ('survivor', 'motive')


def get_items_quantity(survivor, survivor_trade_items):
    errors, has_items = Inventory.objects.get(survivor=survivor). \
        calculated_trade_points(survivor_trade_items)
    return errors, has_items


def get_items_points(survivor_trade_items):
    points = 0
    for item in survivor_trade_items:
        points += values[item] * survivor_trade_items[item]
    return points


class TradeSerializer(serializers.ModelSerializer):
    survivor_one_items = serializers.JSONField()
    survivor_two_items = serializers.JSONField()

    class Meta:
        model = Trade
        fields = ('survivor_one', 'survivor_one_items', 'survivor_two', 'survivor_two_items')

    def create(self, validated_data):
        survivor_one = validated_data['survivor_one']
        trade_one = validated_data['survivor_one_items']
        survivor_two = validated_data['survivor_two']
        trade_two = validated_data['survivor_two_items']

        if survivor_one.isInfected:
            raise serializers.ValidationError({"Error": "{} has infected status and lost access to exchange"
                                              .format(survivor_one.name)})
        if survivor_two.isInfected:
            raise serializers.ValidationError({"Error": "{} has infected status and lost access to exchange"
                                              .format(survivor_two.name)})
        if validated_data['survivor_one'] == validated_data['survivor_two']:
            raise serializers.ValidationError({"Error": "the exchange can only be made between different survivors"})
        else:
            errors_one, has_error_one = get_items_quantity(survivor_one, trade_one)
            errors_two, has_error_two = get_items_quantity(survivor_two, trade_two)
            if not has_error_one or not has_error_two:
                raise serializers.ValidationError(
                    {"Error": errors_one + errors_two})

            points_one = get_items_points(trade_one)
            points_two = get_items_points(trade_two)
            if points_one > points_two:
                raise serializers.ValidationError(
                    {"Error": "the survivor {} has more points than {},the amount must be the same".format(
                        survivor_one.name, survivor_two.name)})
            elif points_two > points_one:
                raise serializers.ValidationError(
                    {"Error": "the survivor {} has more points than {},the amount must be the same".format(
                        survivor_two.name, survivor_one.name)})
            trade = Trade.objects.create(survivor_one=survivor_one,
                                         survivor_two=survivor_two,
                                         survivor_one_items=trade_one,
                                         survivor_two_items=trade_two)
            inventory_one = Inventory.objects.get(survivor=survivor_one)
            inventory_two = Inventory.objects.get(survivor=survivor_two)

            inventory = [inventory_one, inventory_two]
            for inv in inventory:
                for i in trade_one:
                    attr = inv.__getattribute__(i)
                    if inv.survivor == survivor_one:
                        attr -= trade_one[i]
                    else:
                        attr += trade_one[i]
                    inv.__setattr__(i, attr)

                for t in trade_two:
                    attr = inv.__getattribute__(t)
                    if inv.survivor == survivor_one:
                        attr += trade_two[t]
                    else:
                        attr -= trade_two[t]
                    inv.__setattr__(t, attr)
                inv.save()

        return trade


class SurvivorListSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many=False)
    location = LocationSerializer(many=False)

    class Meta:
        model = Survivor
        fields = ('name', 'gender', 'age', 'inventory', 'location')


class SurvivorSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer(many=False)
    location = LocationSerializer(many=False)

    class Meta:
        model = Survivor
        fields = ('name', 'gender', 'age', 'inventory', 'location')

    def create(self, validated_data):
        survivor_data = OrderedDict()
        survivor_fields = ['name', 'gender', 'age']

        for data in survivor_fields:
            survivor_data[data] = validated_data[data]

        inventors_data = validated_data.pop('inventory')
        locations_data = validated_data.pop('location')
        survivor = Survivor.objects.create(**survivor_data)
        Inventory.objects.create(survivor=survivor, **inventors_data)
        Location.objects.create(survivor=survivor, **locations_data)
        return survivor
