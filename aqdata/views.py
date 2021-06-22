from django.views.generic import TemplateView

from rest_framework import mixins, viewsets
from rest_framework.renderers import JSONRenderer

from aqdata import helpers
from aqdata.models import SensorData
from aqdata.serializers import SensorDataSerializer


class HomeView(TemplateView):
    '''
    Home view
    '''
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        '''
        Add the latest sensor data to the context
        '''
        context = super().get_context_data(**kwargs)
        # Make sure data exists before adding extra information to the context
        if SensorData.objects.exists():
            context['latest_sensor_data'] = SensorData.objects.latest('upload_time')
            # Build the trends data
            trends = {
                'BME280_humidity_pc': '', 'BME280_pressure_hpa': '',
                'BME280_temperature_deg_c': '', 'SDS_P1_ppm': '', 'SDS_P2_ppm': ''
            }

            for field in trends:
                # Get the gradient, then translate into a rising, flat, falling
                gradient = helpers.get_data_gradient(field)
                trends[field] = helpers.get_trend(gradient)

            # Add to the context
            context['trends'] = trends

        return context


class SensorDataViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    '''
    Viewset for creating and retrieving `SensorData` entries
    '''
    queryset = SensorData.objects.all()
    renderer_classes = [JSONRenderer]
    serializer_class = SensorDataSerializer

    def create(self, request, *args, **kwargs):
        '''
        Override `create` to preprocess input data before it is serialized
        '''
        request.data.update(helpers.preprocess_uploaded_json(request.data))
        return super().create(request, *args, **kwargs)
