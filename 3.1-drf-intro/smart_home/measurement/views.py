from rest_framework import generics
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorDetailSerializer, MeasurementSerializer, SensorSerializer


class SensView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementView(CreateAPIView):
    queryset = Measurement.objects.filter()
    serializer_class = MeasurementSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)
        sensor_id = request.data.get('sensor')
        temperature = request.data.get('temperature')
        sensor = Sensor.objects.get(id=sensor_id)
        Measurement(id_sensor=sensor, temperature=temperature).save()
        return Response({f'Датчик id={sensor_id}': f'Данные температуры: {temperature}'})
