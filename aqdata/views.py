from rest_framework import mixins, viewsets
from rest_framework.renderers import JSONRenderer

from aqdata.helpers import preprocess_uploaded_json
from aqdata.models import SensorData
from aqdata.serializers import SensorDataSerializer


class SensorDataViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """
    Viewset for creating and retrieving `SensorData` entries
    """
    queryset = SensorData.objects.all()
    renderer_classes = [JSONRenderer]
    serializer_class = SensorDataSerializer

    def create(self, request, *args, **kwargs):
        """
        Override `create` to preprocess input data before it is serialized
        """
        request.data.update(preprocess_uploaded_json(request.data))
        return super().create(request, *args, **kwargs)
