from rest_framework import routers

from upload.views import SensorDataViewSet


router = routers.SimpleRouter()
router.register(r'sensor-data', SensorDataViewSet)
urlpatterns = router.urls
