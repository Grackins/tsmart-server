import time
import socket

from django.db import models


class Device(models.Model):
    ip = models.CharField(
        verbose_name='IP Address',
        max_length=15,
    )
    port = models.IntegerField(
        verbose_name='Port Number',
    )
    name = models.CharField(
        verbose_name='Name',
        max_length=50,
        blank=True,
    )
    status = models.IntegerField(
        verbose_name='Status',
    )

    def send_message(self, msg):
        host = self.ip
        port = self.port
        server = (host, port)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect(server)
            s.send(msg.encode())
            resp = s.recv(1024).decode()
            s.close()
            return resp
        except Exception:
            self.status = 2
            self.save()
        return ''

    def change_status(self, status):
        msg = str(status) * 3 + '\n'
        result = self.send_message(msg).strip()
        if len(result) != 1 or result[0] not in '01':
            return False
        self.notify_status(1 if result[0] == '1' else 0)
        return True

    def notify_status(self, status):
        self.status = status
        self.save()

    def update_status(self):
        msg = '???\n'
        result = self.send_message(msg).strip()
        if len(result) != 1 or result[0] not in '01':
            return False
        self.notify_status(1 if result[0] == '1' else 0)
        return True
