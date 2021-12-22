from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.decorators.http import require_http_methods
from .models import Device


def home_view(request):
    devices = Device.objects.all()
    return render(
        request,
        'devman/devman_index.html',
        {
            'ldevs': devices[0::2],
            'rdevs': devices[1::2],
        },
    )


@require_http_methods(['POST'])
def settings_view(request):
    print(request.POST)
    dev_id = int(request.POST.get('dev_id', '-1'))
    status = int(request.POST.get('status', '-1'))
    if dev_id == -1 or status not in [0, 1]:
        return HttpResponseBadRequest('Bad request')
    device = get_object_or_404(Device, pk=dev_id)
    if not device.change_status(status):
        return HttpResponse(status=503)
    return HttpResponse(status=200)
