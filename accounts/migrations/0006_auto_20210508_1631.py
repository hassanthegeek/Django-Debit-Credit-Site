# Generated by Django 3.1.5 on 2021-05-08 11:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20210508_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountdetail',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account'),
        ),
        migrations.AlterField(
            model_name='accountdetail',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.shop'),
        ),
    ]
