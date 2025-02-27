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
        total = 0

        def create_level(manager=None, level=0):
            nonlocal total

            if total >= self.TOTAL or level == self.LEVELS:
                return

            subordinates = []
            for _ in range(random.randint(5, 20) if manager else 1):
                subordinates.append(Employee(
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    patronymic=fake.first_name_male(),
                    position=fake.job(),
                    hire_date=fake.date_between(start_date='-10y', end_date='today'),
                    email=fake.unique.email(),
                    level=level,
                    manager=manager
                ))

            Employee.objects.bulk_create(subordinates)
            total += len(subordinates)
            for emp in subordinates:
                create_level(emp, level + 1)

        create_level()
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded the database in {time.time() - start_time:.2f}s'))
