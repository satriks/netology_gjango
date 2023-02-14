from django.urls import path

from measurement.views import SensView, SensorView, MeasurementView

urlpatterns = [
    path('sensors/', SensView.as_view()),
    path('sensors/<pk>', SensorView.as_view()),
    path('measurements', MeasurementView.as_view()),
]
