from django.urls import path
from . import views

urlpatterns = [
        path('', views.devman_home_view),
        path('secdev/toggle', views.toggle_secdevice_view),
        path('secdev/logs', views.secdevice_logs_view),
        path('secdev/alarm', views.secdevice_submit_alarm_view),
        ]
