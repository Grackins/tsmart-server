from django.db import models

class SecDevice(models.Model):
    ip = models.CharField(
            verbose_name='IP Address',
            max_length=15,
            )
    port = models.IntegerField(
            verbose_name='Port Number',
            )


class SecAlarm(models.Model):
    time = models.DateTimeField(
            verbose_name='Time',
            )
    device = models.ForeignKey(
            SecDevice,
            verbose_name='Device',
            on_delete=models.CASCADE
            )
