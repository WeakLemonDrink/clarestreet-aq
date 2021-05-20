from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    '''
    Index view
    '''

    print('Headers: {}'.format(request.headers))
    print('GET: {}'.format(request.GET))
    print('POST: {}'.format(request.POST))
    print('FILES: {}'.format(request.FILES))
    print('body: {}'.format(request.body))

    '''
    Headers: {'Content-Length': '473', 'Content-Type': 'application/json', 'Host': '192.168.0.4:8000', 'User-Agent': 'NRZ-2020-133/14907210/3c6105e3774a', 'Accept-Encoding': 'identity;q=1,chunked;q=0.1,*;q=0', 'Connection': 'close', 'X-Sensor': 'esp8266-14907210', 'X-Mac-Id': 'esp8266-3c6105e3774a'}
    GET: <QueryDict: {}>
    POST: <QueryDict: {}>
    FILES: <MultiValueDict: {}>
    body: b'{"esp8266id": "14907210", "software_version": "NRZ-2020-133", "sensordatavalues":[{"value_type":"SDS_P1","value":"16.85"},{"value_type":"SDS_P2","value":"4.35"},{"value_type":"BMP280_pressure","value":"102184.50"},{"value_type":"BMP280_temperature","value":"9.27"},{"value_type":"samples","value":"5003746"},{"value_type":"min_micro","value":"28"},{"value_type":"max_micro","value":"20049"},{"value_type":"interval","value":"145000"},{"value_type":"signal","value":"-85"}]}'
    '''

    return HttpResponse("Hello, world. You're at the upload index.", status=200)
