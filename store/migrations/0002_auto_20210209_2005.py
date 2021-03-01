# Generated by Django 3.1.5 on 2021-02-09 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('M&F', 'Meat and Fish'), ('F&V', 'Fruits and Vegetables'), ('Cooking', 'Cooking'), ('Beverages', 'BEVERAGES'), ('H&C', 'Home and Cleaning'), ('Pest Control', 'Pest Control'), ('Ofc Prod', 'Office Products'), ('Bt Prod', 'Beauty Products'), ('Hea Prod', 'Health Products'), ('PetCare', 'Pet Care'), ('Home App', 'Home Appliances'), ('Babycare', 'Baby Care'), ('fashion', 'Fashion')], max_length=20),
        ),
    ]