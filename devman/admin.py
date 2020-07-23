from django.contrib import admin
from .models import SecDevice, SecAlarm, WeatherDevice

class SecDeviceAdmin(admin.ModelAdmin):
    pass


class SecAlarmAdmin(admin.ModelAdmin):
    pass


class WeatherDeviceAdmin(admin.ModelAdmin):
    pass


admin.site.register(SecDevice, SecDeviceAdmin)
admin.site.register(SecAlarm, SecAlarmAdmin)
admin.site.register(WeatherDevice, WeatherDeviceAdmin)

