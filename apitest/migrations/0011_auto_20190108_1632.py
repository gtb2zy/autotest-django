# Generated by Django 2.1.2 on 2019-01-08 08:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apitest', '0010_auto_20190108_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apistep',
            name='Apitest',
        ),
        migrations.RemoveField(
            model_name='apitest',
            name='Product',
        ),
        migrations.DeleteModel(
            name='Apistep',
        ),
        migrations.DeleteModel(
            name='Apitest',
        ),
    ]
