# Generated by Django 2.1.2 on 2019-01-17 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0019_auto_20190115_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='apis',
            name='level',
            field=models.IntegerField(default=-1, verbose_name='测试基本'),
        ),
    ]
