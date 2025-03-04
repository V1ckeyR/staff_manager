from django.urls import path

from employees.views import employees, get_top_managers, EmployeeHierarchyView

urlpatterns = [
    path('', employees, name='employees'),
    path('employees/', get_top_managers, name='get_top_managers'),
    path('employees/<int:employee_id>/subordinates/', EmployeeHierarchyView.as_view(), name='load_subordinates')
]