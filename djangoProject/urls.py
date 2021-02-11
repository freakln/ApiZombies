from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'survivor', views.SurvivorRecordViewSet)
router.register(r'location', views.LocationRecordViewSet)
router.register(r'report', views.ReportRecordViewSet)
router.register(r'trade', views.TradeRecordViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
