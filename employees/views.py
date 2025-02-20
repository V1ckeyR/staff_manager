from django.core.paginator import Paginator
from django.shortcuts import render

from employees.models import Employee


def employees(request):
    top_managers = Employee.objects.filter(manager__isnull=True)
    paginator = Paginator(top_managers, 20)

    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)

    avatar = ['img/male_avatar.svg', 'img/female_avatar.svg']
    colors = ['primary', 'success', 'danger', 'warning', 'info']
    return render(request, 'index.html', {"colors": colors, "avatar": avatar, "employees": page})
