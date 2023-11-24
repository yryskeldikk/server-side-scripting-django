from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator


class Bank(models.Model):
    name = models.CharField(max_length=200)
    swift_code = models.CharField(max_length=200)
    inst_num = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=200)
    transit_num = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    email = models.EmailField(
        max_length=200,
        default="admin@utoronto.ca",
        validators=[EmailValidator(message="Enter a valid email address.")],
    )
    capacity = models.PositiveIntegerField(blank=True, null=True)
    last_modified = models.DateTimeField(auto_now=True)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)

    def __str__(self):
        return self.name    
