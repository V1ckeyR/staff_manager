import random
import time

from django.core.management import BaseCommand
from faker import Faker

from employees.models import Employee


class Command(BaseCommand):
    help = 'Seed the database with employee data'
    TOTAL = 50000
    LEVELS = 7

    def handle(self, *args, **kwargs):
        start_time = time.time()
        Employee.objects.all().delete()  # Clear table

        fake = Faker()
        employees_per_level = self.TOTAL // self.LEVELS
        employees = []
        for level in range(self.LEVELS):
            amount = employees_per_level if level < self.LEVELS - 1 else self.TOTAL - len(employees)
            new_employees = []
            for _ in range(amount):
                manager = random.choice(employees) if employees else None
                new_employees.append(Employee(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    patronymic=fake.first_name_male(),
                    position=fake.job(),
                    hire_date=fake.date_between(start_date='-10y', end_date='today'),
                    email=fake.unique.email(),
                    manager=manager
                ))

            Employee.objects.bulk_create(new_employees)
            employees.extend(Employee.objects.filter(id__in=[e.id for e in new_employees]))

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded the database in {time.time() - start_time:.2f}s'))
