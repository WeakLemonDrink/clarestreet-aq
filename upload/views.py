from django.views.decorators.csrf import csrf_exempt

from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from upload.helpers import preprocess_uploaded_json
from upload.serializers import SensorDataSerializer


@csrf_exempt
@api_view(('POST',))
@renderer_classes((JSONRenderer,))
def upload(request):
    '''
    View to receive incoming json data and save to new `SensorData` entries if the data is valid
    '''

    # Return bad request by default
    context = ''
    response_status = status.HTTP_400_BAD_REQUEST

    # Decode incoming json and then pass to serializer
    serializer = SensorDataSerializer(data=preprocess_uploaded_json(request.body))

    if serializer.is_valid():
        # If incoming data is valid, save to `SensorData`
        serializer.save()
        response_status = status.HTTP_201_CREATED
    else:
        # Return errors
        context = serializer.errors

    return Response(context, status=response_status)
