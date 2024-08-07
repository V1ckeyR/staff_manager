from django.core.exceptions import ValidationError
from django.db import models


class Employee(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    hire_date = models.DateField()
    email = models.EmailField(unique=True)
    manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subordinates')

    class Meta:
        indexes = [
            models.Index(fields=['manager'])
        ]

    def save(self, *args, **kwargs):
        if self.manager == self:  # To prevent circular references
            raise ValidationError("An employee cannot be their own manager.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.patronymic} ({self.email})'
