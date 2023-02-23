from rest_framework import serializers

from django.conf import settings
from students.models import Course


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if len(data) > settings.MAX_STUDENTS_PER_COURSE:
            raise serializers.ValidationError('На курсе уже максимум студентов')
        return data