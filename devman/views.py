from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from .models import SecDevice


def devman_home_view(request):
    return render(request,
            'devman/devman_index.html',
            {'devs', SecDevice.objects.all()}
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
    return render(request, 'devman/secdevice_logs.html', {'logs': logs})

