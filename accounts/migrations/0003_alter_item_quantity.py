# Generated by Django 4.1.12 on 2023-12-14 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]
