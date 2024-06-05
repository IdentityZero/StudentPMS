from rest_framework import serializers
from .models import Departments, Curriculums, Degrees

class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['department_name']

from .models import Departments, Degrees, Curriculums

class CurriculumsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curriculums
        fields = ['id', 'curriculum_name']

class DegreesSerializer(serializers.ModelSerializer):
    curriculums = CurriculumsSerializer(many=True, read_only=True, source='curriculums_set')

    class Meta:
        model = Degrees
        fields = ['id', 'degree_name', 'curriculums']

class DepartmentsRelatedSerializer(serializers.ModelSerializer):
    degrees = DegreesSerializer(many=True, read_only=True, source='degrees_set')

    class Meta:
        model = Departments
        fields = ['id', 'department_name', 'degrees']