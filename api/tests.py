from .models import *

from rest_framework.test import APITestCase
from rest_framework import status


class SurvivorViewSetTestcase(APITestCase):

    def test_get_survivor(self):
        response = self.client.get('survivor/')
        self.assert_(response.status_code, status.HTTP_201_CREATED)

    def test_create_survivor(self):
        survivor = {
            "name": "testcase",
            "gender": "M",
            "age": 15,
            "inventory": '{"water": 1,"food": 1,"medication": 3,"ammunition": 1}',
            "location": '{"latitude": 15.0,"longitude": 11.0}'
        }
        response = self.client.post('survivor/', data=survivor)
        self.assert_(response.status_code, status.HTTP_201_CREATED)


class ReportViewSetTestcase(APITestCase):
    def test_Create_report(self):
        report = {"survivor": 1, "motive": "teste"}
        response = self.client.post('report/', report)
        self.assert_(response.status_code, status.HTTP_201_CREATED)


class TradeViewSetTestcase(APITestCase):
    survivor_1 = Survivor(name='teste', age=20, gender='M')
    survivor_1.save()
    inventory_1 = Inventory(survivor=survivor_1, water=1, food=1, medication=1, ammunition='1')
    inventory_1.save()
    location_1 = Location(survivor=survivor_1, latitude=10, longitude=10)
    location_1.save()

    survivor_2 = Survivor(name='teste_2', age=20, gender='F')
    survivor_2.save()
    inventory_2 = Inventory(survivor=survivor_2, water=1, food=1, medication=1, ammunition='1')
    location_2 = Location(survivor=survivor_2, latitude=10, longitude=10)
    location_2.save()

    def test_Create_trade(self):
        trade = {"survivor_one": 1, 'survivor_one_items': '{"water": 1, "food": 1, "medication": 1, "ammunition": 1}',
                 "survivor_two": 2, 'survivor_two_items': '{"water": 1, "food": 1, "medication": 1, "ammunition": 1}'}

        response = self.client.post('trade/', data=trade)
        self.assert_(response.status_code, status.HTTP_201_CREATED)


class LocationViewSetTestcase(APITestCase):
    def test_Create_location(self):
        location = {'survivor': 1, "latitude": 1, "longitude": 200}
        response = self.client.post('location/', location)
        self.assert_(response.status_code, status.HTTP_201_CREATED)
