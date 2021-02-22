from django.db.models import Avg, Count, Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from api.serializers import *


class SurvivorRecordViewSet(viewsets.ModelViewSet):
    """Survivor Endpoint
    {
   "name":"text",
   "gender":"M" or "F",
   "age":15,
   "inventory":{
      "water":integer,
      "food": integer,
      "medication":integer,
      "ammunition":integer
   },
   "location":{
      "latitude": float,
      "longitude":float
   }
}


    """

    def list(self, request, *args, **kwargs):
        queryset = Survivor.objects.filter(isInfected=False)
        serializer = SurvivorListSerializer(queryset, many=True)
        return Response(serializer.data)

    queryset = Survivor.objects.all()
    serializer_class = SurvivorSerializer


class LocationRecordViewSet(viewsets.ModelViewSet):
    """
      Location endpoint
      survivor: ID
      latitude: integer
      longitude: integer
      """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    http_method_names = ['get', 'put', 'head']


class ReportRecordViewSet(viewsets.ModelViewSet):
    """
     Report endpoint
     survivor: ID
     motive: "text"
     """
    queryset = ReportInfect.objects.all()
    serializer_class = ReportSerializer


class TradeRecordViewSet(viewsets.ModelViewSet):
    """
     Trade endpoint
     survivor_one:2
    survivor_one_items:{"water":1}
    survivor_two:3
    survivor_two_items:{"water":1}}
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
