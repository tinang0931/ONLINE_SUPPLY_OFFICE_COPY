import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
import csv
from django.shortcuts import render, redirect
from .config import CAMPUS_NAME, SITE_TITLE, HEADING_TEXT, SUBHEADING_TEXT




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

def ppmp(request):
    context = {
        'CAMPUS_NAME': CAMPUS_NAME,
        'SITE_TITLE': SITE_TITLE
    }
    return render(request, 'accounts/User/ppmp.html', context)

def catalogue(request):
    
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
