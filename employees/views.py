from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from employees.models import Employee
from employees.serializers import EmployeeSerializer


@api_view(["GET"])
def load_subordinates(request, employee_id):
    try:
        employee = Employee.objects.get(id=employee_id)
        subordinates = employee.subordinates.all()
        serializer = EmployeeSerializer(subordinates, many=True, context={"depth": 0})
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)


def employees(request):
    top_managers = Employee.objects.prefetch_related("subordinates").filter(manager=None)
    serializer = EmployeeSerializer(top_managers, many=True, context={"depth": 0})

    # print(serializer.data)
    # top_managers = Employee.objects.filter(level__lte=2)

    # paginator = Paginator(top_managers, 20)
    # page_number = request.GET.get("page")
    # page = paginator.get_page(page_number)

    colors = ['primary', 'success', 'danger', 'warning', 'info']
    return render(request, 'index.html', {"colors": colors, "data": serializer.data})
