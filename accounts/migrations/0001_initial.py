# Generated by Django 4.1.13 on 2024-09-27 00:28

from decimal import Decimal
from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=12, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=12)),
                ('last_name', models.CharField(max_length=12)),
                ('contact1', models.PositiveIntegerField()),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('budget', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('regular', 'Regular User'), ('cd', 'Campus Director'), ('budget', 'Budget Officer'), ('bac', 'BAC')], max_length=15)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_regular', models.BooleanField(default=False)),
                ('is_cd', models.BooleanField(default=False)),
                ('is_budget', models.BooleanField(default=False)),
                ('is_bac', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('pr_id', models.CharField(max_length=50, unique=True)),
                ('submission_date', models.DateField(auto_now_add=True)),
                ('bac_status', models.CharField(max_length=20)),
                ('bo_status', models.CharField(max_length=20)),
                ('bo_comment', models.TextField(blank=True, null=True)),
                ('bo_approved_date', models.DateTimeField(blank=True, null=True)),
                ('cd_status', models.CharField(max_length=20)),
                ('cd_comment', models.TextField(blank=True, null=True)),
                ('cd_approved_date', models.DateTimeField(blank=True, null=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('year', 'user')},
            },
        ),
        migrations.CreateModel(
            name='CSV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.CharField(max_length=255)),
                ('Item_name', models.CharField(max_length=255)),
                ('Item_Brand', models.CharField(max_length=255)),
                ('Unit', models.CharField(max_length=50)),
                ('Price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('item_id', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileMetadata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='file_uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='VerificationCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('code', models.CharField(max_length=4)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PR_Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(blank=True, max_length=255, null=True)),
                ('item_brand_description', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('submission_date', models.DateField(auto_now_add=True)),
                ('total_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.checkout')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Pr_identifier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_date', models.DateField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('pr_id', models.CharField(blank=True, max_length=8, null=True, unique=True)),
                ('purpose', models.TextField(blank=True, null=True)),
                ('bo_status', models.CharField(max_length=20)),
                ('bo_comment', models.TextField(blank=True, null=True)),
                ('bo_approved_date', models.DateTimeField(blank=True, null=True)),
                ('cd_status', models.CharField(max_length=20)),
                ('cd_comment', models.TextField(blank=True, null=True)),
                ('cd_approved_date', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PR',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
                ('item', models.CharField(blank=True, max_length=255, null=True)),
                ('item_brand_description', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('quantity', models.IntegerField()),
                ('total_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('metadata', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.filemetadata')),
                ('pr_identifier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.pr_identifier')),
            ],
        ),
        migrations.CreateModel(
            name='PPMP',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item', models.CharField(blank=True, max_length=255, null=True)),
                ('item_brand_description', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('submission_date', models.DateField(auto_now_add=True)),
                ('total_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('jan', models.IntegerField(default=0)),
                ('feb', models.IntegerField(default=0)),
                ('mar', models.IntegerField(default=0)),
                ('apr', models.IntegerField(default=0)),
                ('may', models.IntegerField(default=0)),
                ('jun', models.IntegerField(default=0)),
                ('jul', models.IntegerField(default=0)),
                ('aug', models.IntegerField(default=0)),
                ('sep', models.IntegerField(default=0)),
                ('oct', models.IntegerField(default=0)),
                ('nov', models.IntegerField(default=0)),
                ('dec', models.IntegerField(default=0)),
                ('estimate_budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item', models.CharField(blank=True, max_length=255, null=True)),
                ('item_brand_description', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('submission_date', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_request_id', models.CharField(max_length=20)),
                ('date_requested', models.DateField()),
                ('purpose', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('status_description', models.CharField(max_length=200)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CheckoutItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(blank=True, max_length=255, null=True)),
                ('item_brand_description', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('jan', models.IntegerField(default=0)),
                ('feb', models.IntegerField(default=0)),
                ('mar', models.IntegerField(default=0)),
                ('apr', models.IntegerField(default=0)),
                ('may', models.IntegerField(default=0)),
                ('jun', models.IntegerField(default=0)),
                ('jul', models.IntegerField(default=0)),
                ('aug', models.IntegerField(default=0)),
                ('sep', models.IntegerField(default=0)),
                ('oct', models.IntegerField(default=0)),
                ('nov', models.IntegerField(default=0)),
                ('dec', models.IntegerField(default=0)),
                ('estimate_budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('checkout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.checkout')),
            ],
        ),
        migrations.CreateModel(
            name='appr_ppmp',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item', models.CharField(blank=True, max_length=255, null=True)),
                ('item_brand_description', models.CharField(blank=True, max_length=255, null=True)),
                ('unit', models.CharField(blank=True, max_length=50, null=True)),
                ('unit_cost', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('submission_date', models.DateField(auto_now_add=True)),
                ('jan', models.IntegerField(default=0)),
                ('feb', models.IntegerField(default=0)),
                ('mar', models.IntegerField(default=0)),
                ('apr', models.IntegerField(default=0)),
                ('may', models.IntegerField(default=0)),
                ('jun', models.IntegerField(default=0)),
                ('jul', models.IntegerField(default=0)),
                ('aug', models.IntegerField(default=0)),
                ('sep', models.IntegerField(default=0)),
                ('oct', models.IntegerField(default=0)),
                ('nov', models.IntegerField(default=0)),
                ('dec', models.IntegerField(default=0)),
                ('estimate_budget', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10)),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('comment', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
