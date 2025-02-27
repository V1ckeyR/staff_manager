from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from employees.views import employees, load_subordinates

urlpatterns = [
    path('', employees, name='employees'),
    path('employees/<int:employee_id>/subordinates/', load_subordinates, name='load_subordinates')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)