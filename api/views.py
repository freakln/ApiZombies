from django.db.models import Avg, Count, Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import *


class SurvivorRecordViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset = Survivor.objects.filter(isInfected=False)
        serializer = SurvivorListSerializer(queryset, many=True)
        return Response(serializer.data)

    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer


class LocationRecordViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    http_method_names = ['get', 'put', 'head']


class ReportRecordViewSet(viewsets.ModelViewSet):
    queryset = ReportInfect.objects.all()
    serializer_class = ReportSerializer


class TradeRecordViewSet(viewsets.ModelViewSet):
    """
     Trade endpoint
     Survivor:ID
     trade items : {water:amount,food:amount}
     """
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer


class ApiReport(APIView):
    """

    Percentage of infected survivors.
    Percentage of non-infected survivors.
    Average amount of each kind of resource by survivor (e.g. 5 waters per survivor)
    Points lost because of infected survivor.

    """

    def get(self, request, format=None):
        percent_infect = (Survivor.objects.filter(isInfected=True).count() / Survivor.objects.count()) * 100
        percent_non_infect = (Survivor.objects.filter(isInfected=False).count() / Survivor.objects.count()) * 100
        avg = Inventory.objects.all().aggregate(Avg('water'), Avg('food'), Avg('medication'), Avg('ammunition'))
        points = Inventory.objects.filter(survivor__isInfected=True).aggregate(total=(Sum('water') * 4 +
                                                                                      Sum('food') * 3 +
                                                                                      Sum('medication') * 2 +
                                                                                      Sum('ammunition') * 1))
        resp = []
        for item in avg:
            resp.append('{:.2f} {}s per survivor'.format(avg[item], item[:-5]))


        response = ('Now we have {:.2f}% survivor infected'.format(percent_infect),
                    'Now we have {:.2f}% survivor alive and safe'.format(percent_non_infect),
                    'Average amount inventory from survivors',
                    resp,
                    'number of trade points lost in lost inventories of infected survivors: {}'.format(points['total']))
        return Response(response)
