# Generated by Django 5.0 on 2024-01-09 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_attachment_remove_checkoutitems_attached_file'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Attachment',
        ),
        migrations.AddField(
            model_name='checkoutitems',
            name='attached_file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
