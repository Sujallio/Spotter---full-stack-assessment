from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from trip.views import TripViewSet, ELDLogViewSet

router = DefaultRouter()
router.register(r'trips', TripViewSet)
router.register(r'eld-logs', ELDLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
