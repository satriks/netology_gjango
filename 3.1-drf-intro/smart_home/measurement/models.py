from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, default='')


class Measurement(models.Model):
    id_sensor = models.ForeignKey('Sensor', on_delete=models.CASCADE, related_name="measurements")
    temperature = models.FloatField()
    date_info = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='.', blank=True, default='')
