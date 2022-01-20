import datetime
from django.db import models
from users.models import CustomUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Shop(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=40)
    phone = PhoneNumberField(unique=True)
    address = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return f'{self.name} --- {self.user.username}'


class Account(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    date_created = models.DateTimeField(
        blank=False, auto_now_add=True, null=False)

    def __str__(self) -> str:
        return f'{self.user.username} -- {self.date_created}'


class AccountDetail(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    date = models.DateTimeField(blank=False, null=False, auto_now_add=True)
    remarks = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return str(self.amount)
