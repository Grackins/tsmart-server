from django.contrib import admin
from .models import SecDevice, SecAlarm

class SecDeviceAdmin(admin.ModelAdmin):
    pass


class SecAlarmAdmin(admin.ModelAdmin):
    pass


admin.site.register(SecDevice, SecDeviceAdmin)
admin.site.register(SecAlarm, SecAlarmAdmin)

