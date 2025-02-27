from rest_framework import serializers

from employees.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    subordinates = serializers.SerializerMethodField()
    has_more_subordinates = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = '__all__'

    def get_full_name(self, obj):
        return f"{obj.patronymic} {obj.first_name} {obj.last_name}"

    def get_subordinates(self, obj):
        if self.context.get("depth", 1) >= 2:
            return []
        subordinates = obj.subordinates.all()
        return EmployeeSerializer(subordinates, many=True, context={"depth": self.context.get("depth", 1) + 1}).data

    def get_has_more_subordinates(self, obj):
        return obj.subordinates.filter(subordinates__isnull=False).exists()
