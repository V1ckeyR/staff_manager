from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from employees.models import Employee
from employees.serializers import EmployeeSerializer, ErrorResponseSerializer


COLORS = ['primary', 'success', 'danger', 'warning', 'info']

@extend_schema(responses={
    200: EmployeeSerializer(many=True)
})
@api_view(["GET"])
def get_top_managers(request):
    top_managers = Employee.objects.prefetch_related("subordinates").filter(manager=None)
    serializer = EmployeeSerializer(top_managers, many=True, context={'max_depth': 2})
    return Response(serializer.data)

def employees(request):
    top_managers = get_top_managers(request).data
    return render(request, 'index.html', {"colors": COLORS, "data": top_managers})

class EmployeeHierarchyView(APIView):
    @extend_schema(
        responses={
            (200, "application/json"): EmployeeSerializer(many=True),
            (200, "text/html"): str,
            400: ErrorResponseSerializer(),
            404: ErrorResponseSerializer()
        }
    )
    def get(self, request, employee_id):
        headers = request.headers.get("Accept", "")
        try:
            employee = Employee.objects.get(id=employee_id)
            subordinates = employee.subordinates.all()
            data = EmployeeSerializer(subordinates, many=True).data
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=404)
        else:
            if "application/json" in headers:
                return Response(data)
            if "text/html" in headers:
                return render(request, 'subordinates.html', {"colors": COLORS, "data": data})
        return Response({"error": "Unknown Accept header"}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeView(ViewSet):
    pass
    # paginator = Paginator(top_managers, 20)
    # page_number = request.GET.get("page")
    # page = paginator.get_page(page_number)
