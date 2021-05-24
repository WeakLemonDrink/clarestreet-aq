from rest_framework.viewsets import ModelViewSet

from upload.helpers import preprocess_uploaded_json
from upload.models import SensorData
from upload.serializers import SensorDataSerializer


class SensorDataViewSet(ModelViewSet):  # pylint:disable=too-many-ancestors
    """
    Viewset for creating and retrieving `SensorData` entries
    """
    queryset = SensorData.objects.all()
    serializer_class = SensorDataSerializer

    def create(self, request, *args, **kwargs):
        """
        Override `create` to preprocess input data before it is serialized
        """
        request.data.update(preprocess_uploaded_json(request.data))
        return super().create(request, *args, **kwargs)
