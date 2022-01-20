from django.contrib import admin
from .models import Shop, Account, AccountDetail
# Register your models here.


admin.site.register(Shop)
admin.site.register(Account)
admin.site.register(AccountDetail)


def time_seconds(self, obj):
    return obj.timefield.strftime("%d %b %Y %H:%M:%S")


time_seconds.short_description = 'Precise Time'

list_display = ('id', 'time_seconds', )
