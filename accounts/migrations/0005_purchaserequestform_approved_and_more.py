# Generated by Django 4.1.11 on 2023-12-12 02:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_checkout_is_approve'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaserequestform',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='purchaserequestform',
            name='disapproved',
            field=models.BooleanField(default=False),
        ),
    ]
