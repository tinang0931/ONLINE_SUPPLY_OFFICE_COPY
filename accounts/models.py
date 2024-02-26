from dynamorm import DynamModel
from marshmallow import Schema, fields
from django.conf import settings


class User(DynamModel):
    class Table:
        resource_kwargs = {
            'endpoint_url': settings.DB_ENDPOINT
        }
        
        name = settings.DB_TABLE
        hash_key = 'user_id'
        read = True
        write = True
        
    class Schema:
        user_id = fields.Str()
        username = fields.Str()
        first_name = fields.Str()
        last_name = fields.Str()
        contact1 = fields.Str()
        email = fields.Email()
        
        
    user_type = {
        'admin': 'Admin',
        'regular': 'Regular user',
        'cd': 'Campus Director',
        'budget': 'Budget Officer',
        'bac': 'BAC'
        
    }
    
    user_type = fields.Str(choices=user_type)
    
class Item(DynamModel):
    class Table:
        resource_kwargs = {
            'endpoint_url': settings.DB_ENDPOINT
        }
        
        name = settings.DB_TABLE
        hash_key = 'item_id'
        read = True
        write = True
        
    class Schema:
        item_id = fields.Str()
        item_name = fields.Str()
        quantity = fields.Int()
        unit = fields.Str()
        unit_cost = fields.Str()
        item_brand_description = fields.Str()
        
        
class PPMP(DynamModel):
    class Table:
        resource_kwargs = {
            'endpoint_url': settings.DB_ENDPOINT
        }
        
        name = settings.DB_TABLE
        hash_key = 'ppmp_id'
        read = True
        write = True
        
    class Schema:
        ppmp_id = fields.Str()
        ppmp_name = fields.Str()
        ppmp_description = fields.Str()
        ppmp_date = fields.Str()

class PR_Item(DynamModel):
    class Table:
        resource_kwargs = {
            
            'endpoint_url': settings.DB_ENDPOINT
        }
        
        name = settings.DB_TABLE
        hash_key = 'pr_id'
        read = True
        write = True
    
    class Schema:
        pr_id = fields.Str()
        item = fields.Str()
        item_brand_description = fields.Str()
        unit = fields.Str()
        unit_cost = fields.Str()
        quantity = fields.Int()
        total_cost = fields.Int()


def PR(DynamModel):
    class Table:
        resource_kwargs = {
            'endpoint_url': settings.DB_ENDPOINT
        }
    
        name = settings.DB_TABLE
        hash_key = 'pr_id'
        read = True
        write = True
        
    class Schema:
        pr_id = fields.Str()
        item = fields.Str()
        item_brand_description = fields.Str()
        unit = fields.Str()
        unit_cost = fields.Str()
        quantity = fields.Int()
        total_cost = fields.Int()

def PR_identifier(DynamModel):
    class Table:
        resource_kwargs = {
            'endpoint_url': settings.DB_ENDPOINT
            
        }
        
        name = settings.DB_TABLE
        hash_key = 'pr_id'
        read = True
        write = True
    
    class Schema:
        pr_id = fields.Str()
        purpose = fields.Str()

class Checkout(DynamModel):
    class Table:
        resource_kwargs = {
            'endpoint_url': settings.DB_ENDPOINT
        }

        name = settings.DB_TABLE
        
        hash_key = 'pr_id'
        read = True
        write = True
        
    class Schema:
        pr_id = fields.Str()
        item = fields.Str()
        item_brand_description = fields.Str()
        unit = fields.Str()
        unit_cost = fields.Str()
        quantity = fields.Int()
        total_cost = fields.Int()

def CheckoutItems(DynamModel):
    class Table:
        resource_kwargs = {
            
            'endpoint_url': settings.DB_ENDPOINT
        }
        
    
        name = settings.DB_TABLE
        hash_key = 'pr_id'
        read = True
        write = True
        
    class Schema:
        pr_id = fields.Str()
        item = fields.Str()
        item_brand_description = fields.Str()
        unit = fields.Str()
        unit_cost = fields.Str()
        quantity = fields.Int()
        total_cost = fields.Int()
        
def FileMetadata(DynamModel):
    class Table:
        resource_kwargs = {
            
            'endpoint_url': settings.DB_ENDPOINT
        }
    
        name = settings.DB_TABLE
        hash_key = 'filename'
        read = True
        write = True
        
    class Schema:
        filename = fields.Str()
        file = fields.Str()

def CSV(DynamModel):
    class Table:
        resource_kwargs = {
            
            'endpoint_url': settings.DB_ENDPOINT
        }
        
        name = settings.DB_TABLE
        hash_key = 'item_id'
        read = True
        
    class Schema:
        item_id = fields.Str()
        item_name = fields.Str()
        quantity = fields.Int()
        unit = fields.Str()
        unit_cost = fields.Str()
        item_brand_description = fields.Str()
        
class Category(DynamModel):
    class Table:
        resource_kwargs = {
            
            'endpoint_url': settings.DB_ENDPOINT
            
        }
        
        name = settings.DB_TABLE
        hash_key = 'category'
        read = True
        write = True
        
    class Schema:
        category = fields.Str()
        description = fields.Str()
        







