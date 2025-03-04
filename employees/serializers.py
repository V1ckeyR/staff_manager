from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    subordinates = serializers.SerializerMethodField()
    has_more_subordinates = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'

    @extend_schema_field(serializers.CharField())
    def get_full_name(self, obj):
        return f"{obj.last_name} {obj.first_name} {obj.patronymic}"

    @extend_schema_field(serializers.JSONField())
    def get_subordinates(self, obj):
        if self.context.get('depth', 0) >= self.context.get('max_depth', 0):
            return []
        subordinates = obj.subordinates.all()
        context = {'depth': self.context.get('depth', 0) + 1, 'max_depth': self.context.get('max_depth', 0)}
        return EmployeeSerializer(subordinates, many=True, context=context).data

    @extend_schema_field(serializers.BooleanField())
    def get_has_more_subordinates(self, obj):
        return obj.subordinates.filter(subordinates__isnull=False).exists()
