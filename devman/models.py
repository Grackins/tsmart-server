from django.db import models
import time
import socket

class Device(models.Model):
    ip = models.CharField(
            verbose_name='IP Address',
            max_length=15,
            )
    port = models.IntegerField(
            verbose_name='Port Number',
            )

    def send_message(self, msg):
        host = self.ip
        port = self.port
        server = (host, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(server)
        s.send(msg.encode('utf-8'))
        resp = s.recv(1024)
        s.close()
        return resp


class SecDevice(Device):
    status = models.BooleanField(
            default=False,
            )

    def toggle_status(self):
        self.status = not self.status
        while self.send_message('1' if self.status else '0') != b'OK\n':
            time.sleep(1)
        self.save()


class SecAlarm(models.Model):
    time = models.DateTimeField(
            verbose_name='Time',
            )
    device = models.ForeignKey(
            SecDevice,
            verbose_name='Device',
            on_delete=models.CASCADE
            )


class WeatherDevice(Device):
    humidity = models.FloatField()
    weather = models.FloatField()

    def update(self):
        info = self.send_message('Get').decode('utf-8').split()
        self.humidity = float(info[0])
        self.weather = float(info[1])
        self.save()

