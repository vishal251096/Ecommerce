# Generated by Django 3.1.5 on 2021-02-27 21:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_auto_20210227_1043'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlist',
            name='product',
        ),
        migrations.RemoveField(
            model_name='orderlist',
            name='quantity',
        ),
    ]
