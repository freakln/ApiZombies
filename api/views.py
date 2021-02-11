from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from api.models import *
from api.serializers import *


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class SurvivorRecordViewSet(viewsets.ModelViewSet):

    def list(self, request, *args, **kwargs):
        queryset = Survivor.objects.all()
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
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer
