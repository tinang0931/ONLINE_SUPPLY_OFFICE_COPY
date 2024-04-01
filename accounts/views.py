import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import csv
from django.shortcuts import render, redirect
from .config import CAMPUS_NAME, SITE_TITLE, HEADING_TEXT, SUBHEADING_TEXT
import time
import random
from datetime import datetime




def landing(request):
    return render(request, 'accounts/User/landing.html')
def userlanding(request):
    context = {
        'HEADING_TEXT': HEADING_TEXT,
        'SUBHEADING_TEXT': SUBHEADING_TEXT
    }
    return render(request, 'accounts/User/userlanding.html', context)

def login(request):
    return render(request, 'accounts/User/login.html')

def reset_password(request):
    return render(request, 'accounts/User/reset_password.html')

def logout_user(request):
    pass

def register(request):
    return render(request, 'accounts/User/register.html')

def ppmp101(request):
    
    context = {
      
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/ppmp101.html', context)

def purchase (request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/purchase.html', context)

def tracker(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/tracker.html', context)

def purchasetracker(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/purchasetracker.html', context)

def about(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/about.html', context)

import boto3
from django.shortcuts import redirect

def ppmp(request):
    if request.method == 'POST':
        year = request.POST.get('selectedYear')
        
    
        items = request.POST.getlist('item')
        item_brands = request.POST.getlist('item_brand')
        units = request.POST.getlist('unit')
        prices = request.POST.getlist('price')
        jans = request.POST.getlist('jan')
        febs = request.POST.getlist('feb')
        mars = request.POST.getlist('mar')
        aprs = request.POST.getlist('apr')
        mays = request.POST.getlist('may')
        juns = request.POST.getlist('jun')
        juls = request.POST.getlist('jul')
        augs = request.POST.getlist('aug')
        seps = request.POST.getlist('sep')
        octs = request.POST.getlist('oct')
        novs = request.POST.getlist('nov')
        decs = request.POST.getlist('dec')
        
        dynamodb = boto3.resource('dynamodb')
        checkout_table = dynamodb.Table('Checkout')
        checkout_items_table = dynamodb.Table('CheckoutItems')
        items_table = dynamodb.Table('Items')
        
        submission_date = datetime.now().strftime("%Y-%m-%d")
        
        # Save data in Checkout table
        pr_id = generate_unique_pr_id() 
        checkout_table.put_item(
            Item={
                'pr_id': pr_id,
                'year': year,
                'submission_date': submission_date
            }
        )
        
   
        for item, item_brand, unit, price, jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec in zip(items, item_brands, units, prices, jans, febs, mars, aprs, mays, juns, juls, augs, seps, octs, novs, decs):
            checkout_items_table.put_item(
                Item={
                    'pr_id': pr_id,
                    'item': item,
                    'item_brand_description': item_brand,
                    'unit': unit,
                    'price': price,
                    'jan': jan,
                    'feb': feb,
                    'mar': mar,
                    'apr': apr,
                    'may': may,
                    'jun': jun,
                    'jul': jul,
                    'aug': aug,
                    'sep': sep,
                    'oct': oct,
                    'nov': nov,
                    'dec': dec
                }
            )
            
            items_table.delete_item(
                Key={
                    'item': item 
                }
            )
            
        
        
        return redirect('tracker')

    else:
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Items')
        
        response = table.scan()
        items = response.get('Items', [])
        print(items)
        context = {
            'items': items,
            'CAMPUS_NAME': CAMPUS_NAME,
            'SITE_TITLE': SITE_TITLE
        }
    return render(request, 'accounts/User/ppmp.html', context)

def generate_unique_pr_id():
    
    timestamp = int(time.time())
    
   
    random_number = random.randint(100, 999)
    
   
    pr_id = f"{timestamp}{random_number}"
    
    return pr_id


def catalogue(request):
    
    if request.method == 'POST':
        item = request.POST.get('item')
        item_brand = request.POST.get('item_brand')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Items')
        
        table.put_item(
            Item={
                'item': item,
                'item_brand_description': item_brand,
                'unit': unit,
                'price': price
            }
        )
        return redirect('catalogue')
    
    else:
    
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('CSV')

        response = table.scan()
        items = response.get('Items', [])

        
        items_by_category = {}
        for item in items:
            category = item.get('Category')
            if category in items_by_category:
                items_by_category[category].append(item)
            else:
                items_by_category[category] = [item]
                
        context = {
            'CAMPUS_NAME': CAMPUS_NAME,
            'SITE_TITLE': SITE_TITLE,
            'items_by_category': items_by_category
        }
        
        return render(request, 'accounts/User/catalogue.html', context )
    

def user_add_new_item(request):
    
    if request.method == 'POST':
        item = request.POST.get('new_item_name')
        item_brand = request.POST.get('new_item_brand')
        unit = request.POST.get('new_item_unit')
        price = request.POST.get('item_unit_price')
        
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table('Items')
        
        table.put_item(
            Item={
                'item': item,
                'item_brand_description': item_brand,
                'unit': unit,
                'price': price
            }
        )
        return redirect('ppmp')
    
   
    return render(request, 'accounts/User/ppmp.html')

def approved_ppmp(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/approved_ppmp.html', context)

def baclanding(request):
    context = {
        'HEADING_TEXT': HEADING_TEXT,
        'SUBHEADING_TEXT': SUBHEADING_TEXT
    }
    return render(request, 'accounts/Admin/BAC_Secretariat/baclanding.html', context)

def bac_home(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_home.html', context)

def bac_request(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_request.html', context)

def bac_dashboard(request):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CSV')

    response = table.scan()
    items = response.get('Items', [])

    
    items_by_category = {}
    for item in items:
        category = item.get('Category')
        if category in items_by_category:
            items_by_category[category].append(item)
        else:
            items_by_category[category] = [item]
            
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE,
        'items_by_category': items_by_category
    }
    
    
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_dashboard.html', context)

def add_new_item(request):
    
    
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/Admin/BAC_Secretariat/add_new_item.html', context)

def bac_about(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_about.html', context)



 

def upload_file(request):
    if request.method == 'POST' and 'file' in request.FILES:
        csv_file = request.FILES['file']
        if csv_file:
            handle_uploaded_file(csv_file)
            return redirect('bac_dashboard')
        
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_dashboard.html')

def handle_uploaded_file(file):
    decode_file = file.read().decode('utf-8')
    csv_data = csv.reader(decode_file.splitlines(), delimiter=',')
    next(csv_data)
    
    category_items = {}  
    for row in csv_data:
        category = row[0]
        item = {
            'item': row[1],
            'item_brand_description': row[2],
            'unit': row[3],
            'price': row[4]
        }
        
        if category in category_items:
            category_items[category].append(item)
        else:
            category_items[category] = [item]
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('CSV')
    for category, items in category_items.items():
        table.put_item(
            Item={
                'Category': category,
                'items': items
            }
        )
        
def delete(request, item):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Items')
    table.delete_item(Key={'item': item})
    return redirect('ppmp')

def bolanding(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/Admin/Budget_Officer/bolanding.html', context)

def bohome(request):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Checkout')
    
    response = table.scan()
    items = response.get('Items', [])
    context = {
        'items': items,
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/Admin/Budget_Officer/bohome.html', context)

def preqform_bo(request, pr_id):
    # Connect to DynamoDB
    dynamodb = boto3.resource('dynamodb')
    checkout_items_table = dynamodb.Table('CheckoutItems')
    
    # Query items associated with the PR ID
    response = checkout_items_table.query(
        KeyConditionExpression='pr_id = :pr_id',
        ExpressionAttributeValues={
            ':pr_id': pr_id
        }
    )
    items = response['Items']
    
    # Pass the items and PR ID to the template
    context = {
        'items': items,
        'pr_id': pr_id
    }

    return render(request, 'accounts/Admin/Budget_Officer/preqform_bo.html', context)
def boabout(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/Admin/Budget_Officer/boabout.html', context)

def boppmp(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/Admin/Budget_Officer/boppmp.html', context)
