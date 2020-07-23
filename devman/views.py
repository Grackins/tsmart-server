from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from datetime import datetime

from .models import SecDevice, SecAlarm
from .utils import get_client_ip


def devman_home_view(request):
    waether_devs = WeatherDevice.objects.all()
    for device in weather_devs:
        device.update()
    return render(
            request,
            'devman/devman_index.html',
            {
                'sec_devs': SecDevice.objects.all(),
                'weather_devs': weather_devs,
                },
            )


@require_http_methods(['GET'])
def toggle_secdevice_view(request):
    dev_id = request.GET.get('device', -1)
    device = get_object_or_404(SecDevice, pk=dev_id)
    device.toggle_status()
    return render(request, 'devman/toggle_secdevice.html', {'device': device})


@require_http_methods(['GET'])
def secdevice_logs_view(request):
    dev_id = request.GET.get('device', -1)
    if dev_id == -1:
        logs = SecAlarm.objects.all()
    else:
        logs = SecAlarm.objects.filter(device_id=dev_id).all()
    return render(request,
            'devman/secdevice_logs.html',
            {'logs': logs},
            )


@require_http_methods(['GET'])
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
    device.update()
    return render(request,
            'devman/watherdevice_view.html',
            {'device': device},
            )

