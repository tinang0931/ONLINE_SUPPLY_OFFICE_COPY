# from django.apps import AppConfig

# class AccountsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'accounts'

from django.apps import AppConfig
from . import dynamodb_setup

class YourAppConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        dynamodb_setup.setup_dynamodb_tables()  # Call the function to set up DynamoDB tables
