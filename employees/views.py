from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from employees.models import Employee
from employees.serializers import EmployeeSerializer


@extend_schema(responses={
    200: EmployeeSerializer(many=True),
    404: {"error": "Employee not found"}
})
@api_view(["GET"])
def load_subordinates(request, employee_id: int):
    try:
        employee = Employee.objects.get(id=employee_id)
        subordinates = employee.subordinates.all()
        serializer = EmployeeSerializer(subordinates, many=True)
        return Response(serializer.data)
    except Employee.DoesNotExist:
        return Response({"error": "Employee not found"}, status=404)


@extend_schema(responses={
    200: EmployeeSerializer(many=True)
})
@api_view(["GET"])
def get_top_managers(request):
    top_managers = Employee.objects.prefetch_related("subordinates").filter(manager=None)
    serializer = EmployeeSerializer(top_managers, many=True, context={'max_depth': 2})
    return Response(serializer.data)

def employees(request):
    # paginator = Paginator(top_managers, 20)
    # page_number = request.GET.get("page")
    # page = paginator.get_page(page_number)

    top_managers = get_top_managers(request).data
    colors = ['primary', 'success', 'danger', 'warning', 'info']
    return render(request, 'index.html', {"colors": colors, "data": top_managers})
