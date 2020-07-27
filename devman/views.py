from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from datetime import datetime

from .models import SecDevice, SecAlarm, WeatherDevice
from .utils import get_client_ip


def devman_home_view(request):
    weather_devs = WeatherDevice.objects.all()
    return render(
            request,
            'devman/devman_index.html',
            {
                'sec_devs': SecDevice.objects.all(),
                'weather_devs': weather_devs,
                },
            )


@require_http_methods(['GET'])
def set_secdevice_view(request):
    dev_id = request.GET.get('device', -1)
    status = request.GET.get('status', '1')
    if status != '0' and status != '1':
        return HttpResponseBadRequest('Bad status')
    device = get_object_or_404(SecDevice, pk=dev_id)
    device.set_status(status == '1')
    return render(request, 'devman/toggle_secdevice.html', {'device': device})


@require_http_methods(['GET'])
def secdevice_logs_view(request):
    dev_id = request.GET.get('device', -1)
    if dev_id == -1:
        logs = SecAlarm.objects
    else:
        logs = SecAlarm.objects.filter(device_id=dev_id)
    logs = logs.order_by('time').reverse().all()
    return render(request,
            'devman/secdevice_logs.html',
            {'logs': logs},
            )


@require_http_methods(['ATGET', 'GET'])
def secdevice_submit_alarm_view(request):
    alarm = SecAlarm()
    device = None
    try:
        device = SecDevice.objects.get(ip=get_client_ip(request))
        alarm.device = device
        alarm.time = datetime.now()
        alarm.save()
        return HttpResponse('OK')
    except Exception:
        return HttpResponse('NOK')


@require_http_methods(['GET'])
def weather_device_view(request):
    dev_id = request.GET.get('device', -1)
    device = get_object_or_404(WeatherDevice, pk=dev_id)
    return render(request,
            'devman/weather_device_view.html',
            {'device': device},
            )


@require_http_methods(['GET'])
def weather_device_update_view(request):
    try:
        device = WeatherDevice.objects.get(ip=get_client_ip(request))
        device.humidity, device.temperature = (float(num) for num in request.GET.get('data').split())
        device.save()
        return HttpResponse('OK')
    except Exception():
        return HttpResponse('NOK')

