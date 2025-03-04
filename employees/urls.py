from django.urls import path

from employees.views import employees, load_subordinates, get_top_managers

urlpatterns = [
    path('', employees, name='employees'),
    path('employees/', get_top_managers, name='get_top_managers'),
    path('employees/<int:employee_id>/subordinates/', load_subordinates, name='load_subordinates')
]