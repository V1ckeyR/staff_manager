from django.urls import path, include
from rest_framework.routers import DefaultRouter

from employees.views import employees, get_top_managers, EmployeeHierarchyView, EmployeeTableView

router = DefaultRouter()
router.register(r"employees_table", EmployeeTableView, basename='employees_table')

urlpatterns = [
    path('', employees, name='employees'),
    path('', include(router.urls)),
    path('employees/', get_top_managers, name='get_top_managers'),
    path('employees/<int:employee_id>/subordinates/', EmployeeHierarchyView.as_view(), name='load_subordinates')
]