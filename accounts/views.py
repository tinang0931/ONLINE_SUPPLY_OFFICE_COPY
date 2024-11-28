
from bson import Decimal128
from decimal import Decimal
import json
from django.core.exceptions import ValidationError
from pymongo import MongoClient
import itertools
from urllib.parse import parse_qs
from django.views import View
from django.http import HttpResponseBadRequest, JsonResponse
from typing import ItemsView
import logging
from django.shortcuts import redirect, render, get_object_or_404
from django.core.cache import cache
from .models import *
import csv
from django.contrib.auth import authenticate, login as auth_login, logout
from .decorators import unauthenticated_user, authenticated_user, admin_required, regular_user_required, bac_required, cd_required, budget_required
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.http import HttpResponse  
from django.shortcuts import render, redirect   
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model
from .tokens import account_activation_token
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.contrib import messages
from django.utils.crypto import get_random_string
from .models import VerificationCode
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import random
from itertools import groupby
from django.core.files.base import ContentFile
from .models import *
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render
from .config import SITE_TITLE, CAMPUS_NAME
from .config import HEADING_TEXT, SUBHEADING_TEXT



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .models import Checkout, CSV, Item
from .serializers import *
import itertools

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

    
        token['username'] = user.username
        token['email'] = user.email

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PPMP101APIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_budget = request.user.budget
            data = Checkout.objects.filter(user=request.user).order_by('-submission_date').first()
            checkouts = Checkout.objects.filter(bo_status='approved', cd_status='approved', user=request.user)
            checkout_serializer = CheckoutSerializer(checkouts, many=True)

            csv_data = CSV.objects.all().order_by('Category')
            grouped_data = {}
            for key, group in itertools.groupby(csv_data, key=lambda x: x.Category):
                grouped_data[key] = CSVSerializer(list(group), many=True).data

            response_data = {
                'user_budget': user_budget,
                'latest_checkout': CheckoutSerializer(data).data if data else None,
                'checkouts': checkout_serializer.data,
                'grouped_data': grouped_data,
                'title': 'DASHBOARD',
            }

       
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'error': 'Failed to fetch PPMP101 data', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PurchaseTrackerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get tracker data for the authenticated user
            tracker = Pr_identifier.objects.filter(user=request.user).order_by('-submission_date')

            # Serialize the tracker data
            serializer = PrIdentifierSerializer(tracker, many=True)

            # Create the response data
            response_data = {
                "tracker": serializer.data,
                "title": "PURCHASE REQUEST TRACKER",
                "CAMPUS_NAME": "Your Campus Name"  # Replace with your campus name or dynamic value
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"error": "Failed to fetch purchase tracker data", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class PPMPTrackerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Get tracker data for the authenticated user
            tracker = Checkout.objects.filter(user=request.user).order_by('-submission_date')

            # Serialize the tracker data
            serializer = CheckoutSerializer(tracker, many=True)

            # Create the response data
            response_data = {
                "checkouts": serializer.data,
                "title": "PURCHASE REQUEST TRACKER",
                "CAMPUS_NAME": "Your Campus Name"  # Replace with your campus name or dynamic value
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"error": "Failed to fetch purchase tracker data", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class ApprovedPPMPAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Filter approved PPMPs for the user
            approved_ppmp = Checkout.objects.filter(
                user=request.user, 
                cd_status='approved', 
                bo_status='approved'
            )

            if approved_ppmp.exists():
                # Filter CheckoutItems related to the approved PPMPs
                checkout_items = CheckoutItems.objects.filter(checkout__in=approved_ppmp)

                # Get the latest year from the approved PPMPs
                latest_year = approved_ppmp.order_by('-year').first().year

                # Response payload
                response_data = {
                    "latest_year": latest_year,
                    "checkouts": CheckoutItemsSerializer(checkout_items, many=True).data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "No approved PPMP found for the user."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"error": "Failed to fetch approved PPMP data", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    def post(self, request):
        try:
            # Validate and extract data from request
            item = request.data.get('item')
            item_brand_description = request.data.get('item_brand_description')
            unit = request.data.get('unit')
            unit_cost = request.data.get('unit_cost')

            if not all([item, item_brand_description, unit, unit_cost]):
                return Response(
                    {"error": "All fields (item, item_brand_description, unit, unit_cost) are required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Convert unit_cost to Decimal
            from decimal import Decimal
            try:
                unit_cost = Decimal(unit_cost)
            except Exception as e:
                return Response(
                    {"error": f"Invalid unit_cost: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create a new CheckoutItem
            checkout_item = PR_Items.objects.create(
                user=request.user,
                item=item,
                item_brand_description=item_brand_description,
                unit=unit,
                unit_cost=unit_cost,
            )

            return Response(
                {"message": "Item added successfully!", "item": PRItemsSerializer(checkout_item).data},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"error": "Failed to add item", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
import random

def generate_unique_pr_id():
    
    while True:
        # Generate a random 8-digit pr_id
        pr_id = random.randint(10000000, 99999999)
        
        # Check if this pr_id already exists in the database
        if not Pr_identifier.objects.filter(pr_id=pr_id).exists():
            return pr_id  # Return the unique pr_id when found

class PurchaseRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            
            purchase_requests = PR_Items.objects.filter(user=request.user)

            if purchase_requests.exists():
                # Serialize the purchase request data
                serializer = PRItemsSerializer(purchase_requests, many=True)
                return Response(
                    {"purchase": serializer.data},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"purchase": [], "message": "No purchase data available"},
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {"error": "Failed to fetch purchase data", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def post(self, request):
        
        # Extract data from the request
        items = request.data.get('items', [])
        item_brands = request.data.get('item_brands', [])
        units = request.data.get('units', [])
        prices = request.data.get('prices', [])
        quantities = request.data.get('quantities', [])
        total_amount = request.data.get('total_amount')
        purpose = request.data.get('purpose')

        # Validate data lengths
        if not (len(items) == len(item_brands) == len(units) == len(prices) == len(quantities)):
            return Response(
                {"error": "All item-related fields must have the same length."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Generate a new PR ID
        pr_id = generate_unique_pr_id()
        user = request.user

        # Create PR Identifier
        pr_identifier = Pr_identifier.objects.create(
            user=user, pr_id=pr_id, purpose=purpose
        )

        # Create PR items
        for i in range(len(items)):
            PR.objects.create(
                pr_identifier=pr_identifier,
                item=items[i],
                item_brand_description=item_brands[i],
                unit=units[i],
                unit_cost=prices[i],
                quantity=quantities[i],
                total_cost=total_amount,
            )

        # Create a new purchase request
        PR_Items.objects.all().delete()
           
        # Response payload
        response_data = {
            "message": "Purchase request created successfully",
            "pr_identifier": PrIdentifierSerializer(pr_identifier).data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

        
class PPMPView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request):
        user_budget = request.user.budget

        purchase_requests = Item.objects.filter(user=request.user)

        serializer = ItemSerializer(purchase_requests, many=True)
        response_data = {
            "budget": user_budget,
            "purchase": serializer.data
        }
        print(response_data)

        return Response(response_data, status=status.HTTP_200_OK)
class CatalogueAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        csv_data = CSV.objects.all().order_by('Category')
        grouped_data = {}
        for key, group in itertools.groupby(csv_data, key=lambda x: x.Category):
            grouped_data[key] = CSVSerializer(list(group), many=True).data

        response_data = {
            'grouped_data': grouped_data,
        }

        return Response(response_data)
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        
        profile = User.objects.get(id=request.user.id)
        serializer = UserSerializer(profile)
        response_data = {
            "profile": serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AddToCartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get data from request body
            item_data = request.data
            item_name = item_data.get('item')
            item_brand_description = item_data.get('item_brand_description')
            unit = item_data.get('unit')
            unit_cost = item_data.get('unit_cost')

            # Validate data
            if not all([item_name, item_brand_description, unit, unit_cost]):
                return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

            # Add item to the cart
            cart_item = Item.objects.create(
                user=request.user,
                item=item_name,
                item_brand_description=item_brand_description,
                unit=unit,
                unit_cost=unit_cost,
            )

            # Return the added item details
            serializer = ItemSerializer(cart_item)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Retrieve the selected year from the request
            selected_year = request.data.get('selectedYear')
            if not selected_year:
                return JsonResponse({'error': 'Selected year is required'}, status=400)

            # Create the checkout record
            new_checkout = Checkout.objects.create(
                user=request.user,
                year=selected_year,
                pr_id=generate_unique_pr_id()
            )

            # Retrieve the item lists and other details from the request
            items = request.data.getlist('item[]')
            item_brands = request.data.getlist('item_brand_description[]')
            units = request.data.getlist('unit[]')
            unit_costs = request.data.getlist('unit_cost[]')

            # Log to see the data being received
            print("Items:", items)
            print("Item Brands:", item_brands)
            print("Units:", units)
            print("Unit Costs:", unit_costs)

            months_data = {
                'jan': request.data.getlist('jan[]'),
                'feb': request.data.getlist('feb[]'),
                'mar': request.data.getlist('mar[]'),
                'apr': request.data.getlist('apr[]'),
                'may': request.data.getlist('may[]'),
                'jun': request.data.getlist('jun[]'),
                'jul': request.data.getlist('jul[]'),
                'aug': request.data.getlist('aug[]'),
                'sep': request.data.getlist('sep[]'),
                'oct': request.data.getlist('oct[]'),
                'nov': request.data.getlist('nov[]'),
                'dec': request.data.getlist('dec[]'),
            }

            # Ensure that data lengths match to avoid index errors
            for i in range(len(items)):
                try:
                    unit_cost_value = float(unit_costs[i])
                    if unit_cost_value <= 0:
                        raise ValueError(f"Invalid unit cost: {unit_cost_value} at index {i}")
                except (ValueError, IndexError):
                    print(f"Skipping item {i} due to invalid or non-numeric unit cost.")
                    continue

                # Skip empty or incomplete items
                if not items[i] or not item_brands[i] or not units[i] or not unit_cost_value:
                    print(f"Skipping item {i} due to missing data.")
                    continue

                # Create CheckoutItems entries
                CheckoutItems.objects.create(
                    checkout=new_checkout,
                    item=items[i],
                    item_brand_description=item_brands[i],
                    unit=units[i],
                    unit_cost=unit_cost_value,
                    jan=months_data['jan'][i] if len(months_data['jan']) > i else '',
                    feb=months_data['feb'][i] if len(months_data['feb']) > i else '',
                    mar=months_data['mar'][i] if len(months_data['mar']) > i else '',
                    apr=months_data['apr'][i] if len(months_data['apr']) > i else '',
                    may=months_data['may'][i] if len(months_data['may']) > i else '',
                    jun=months_data['jun'][i] if len(months_data['jun']) > i else '',
                    jul=months_data['jul'][i] if len(months_data['jul']) > i else '',
                    aug=months_data['aug'][i] if len(months_data['aug']) > i else '',
                    sep=months_data['sep'][i] if len(months_data['sep']) > i else '',
                    oct=months_data['oct'][i] if len(months_data['oct']) > i else '',
                    nov=months_data['nov'][i] if len(months_data['nov']) > i else '',
                    dec=months_data['dec'][i] if len(months_data['dec']) > i else '',
                )

            # Optionally, delete items from the Item model if needed
            Item.objects.filter(user=request.user).delete()

            return JsonResponse({'message': 'Checkout data submitted successfully'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)



def main(request):
    context = {
        'SITE_TITLE': SITE_TITLE,
        'CAMPUS_NAME': CAMPUS_NAME,
    }
    print(CAMPUS_NAME)
    print(SITE_TITLE)
    return render(request, 'accounts/User/main.html', context)



def bac(request):
    return render(request, 'accounts/User/bac.html')

@bac_required
def baclanding(request):
    context ={
        'HEADING_TEXT': HEADING_TEXT,
        'SUBHEADING_TEXT': SUBHEADING_TEXT,
    }
    return render(request, 'accounts/Admin/BAC_Secretariat/baclanding.html', context)

@bac_required
def bac_request(request):

    tracker = Pr_identifier.objects.select_related('user').all()
    context = {
        'tracker': tracker,
        'title': 'PURCHASE REQUESTS',
        'CAMPUS_NAME': CAMPUS_NAME,
  
    }
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_request.html', context)


@cd_required
def cdlanding(request):
    context ={
        'HEADING_TEXT': HEADING_TEXT,
        'SUBHEADING_TEXT': SUBHEADING_TEXT,
    }
    return render(request, 'accounts/Admin/Campus_Director/cdlanding.html', context)


@authenticated_user
def userlanding(request):
    context = {
        'HEADING_TEXT': HEADING_TEXT,
        'SUBHEADING_TEXT': SUBHEADING_TEXT,
    }
    print(HEADING_TEXT)
    print(SUBHEADING_TEXT)
    return render(request, 'accounts/User/userlanding.html', context)


@authenticated_user
def ppmp101(request):
    # Retrieve the current user's budget
    user_budget = request.user.budget

   
    data = Checkout.objects.filter(user=request.user).order_by('-submission_date').first()

    checkouts = Checkout.objects.filter(bo_status='approved', cd_status='approved', user=request.user)
    
    checkout_data = []

    for checkout in checkouts:
        checkout_dict = {
            'year': checkout.year,
            'pr_id': checkout.pr_id,
            'user': checkout.user,
            'submission_date': checkout.submission_date,
        }
        checkout_data.append(checkout_dict)

    grouped_data = {}  # This will hold CSV data grouped by category
    
    # Handle POST request (for adding a new item)
    if request.method == 'POST':
        item_name = request.POST.get(f'item')
        item_brand = request.POST.get(f'item_brand')
        unit = request.POST.get(f'unit')
        price = request.POST.get(f'price')

        # Create the new Item object
        Item.objects.create(
            user=request.user,
            item=item_name,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price
        )

        # Redirect after saving the item
        return redirect('catalogue')

    # Handle GET request (for loading the CSV data)
    elif request.method == 'GET':
        csv_data = CSV.objects.all().order_by('Category')
        for key, group in itertools.groupby(csv_data, key=lambda x: x.Category):
            grouped_data[key] = list(group)

    # Context data to pass to the template
    context = {
        'budget': budget_required,
        'data': data,
        'checkouts': checkout_data,
        'user': request.user,
        'user_budget': user_budget,  # Include the logged-in user's budget
        'grouped_data': grouped_data,
        'title': 'DASHBOARD',
        'CAMPUS_NAME': CAMPUS_NAME,
    }

    # Render the template with the updated context
    return render(request, 'accounts/User/ppmp101.html', context)

def landing(request):
    return render(request, 'accounts/User/landing.html')


@budget_required
def budget_landing(request):
    context = {
        'HEADING_TEXT': HEADING_TEXT,
        'SUBHEADING_TEXT': SUBHEADING_TEXT,
    }
    return render(request, 'accounts/Admin/Budget_Officer/bolanding.html', context)

User = get_user_model()

@unauthenticated_user
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        contact1 = request.POST['contact1']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        budget = request.POST.get('budget')  
        
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/User/login.html')

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email is already in use.")
            return render(request, 'accounts/User/login.html')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password1,
            contact1=contact1,
            is_active=False, 
        )
        user.budget = budget
        user.user_type = 'regular'
        user.is_approved = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('accounts/User/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        messages.success(request, "Registration successful. Please check your email to activate your account.")
        return redirect('login')

    return render(request, 'accounts/User/login.html')

def register_user(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        contact1 = request.POST['contact1']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        user_type = request.POST['user_type']

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/Admin/System_Admin/user.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username or email is already in use.")
            return render(request, 'accounts/Admin/System_Admin/user.html')
            

        user = User.objects.create_user(username=username, email=email, password=password1, contact1=contact1, user_type=user_type, is_active=False)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('accounts/User/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        return redirect('user')
    return render(request, 'accounts/Admin/System_Admin/user.html')

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can log in to your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    

def approve_user(request):
    all_users = User.objects.all()
    

    # Get all unapproved regular users
    unapproved_users = []
    for user in all_users:
        if not user.is_approved:
            if user.is_regular:  # Regular users need manual approval
                unapproved_users.append(user)
            else:  # Non-regular users are automatically approved
                user.is_approved = True
                user.budget = 0  # Set budget to 0 for non-regular users
                user.save()  # Save changes to the user
                messages.success(request, f"Non-regular user {user.username} automatically approved.")

    if request.method == 'POST':
        username = request.POST.get('user_id')  # Fetch the username from the form
        budget = request.POST.get('budget')

        try:
            # Find the user using the username (primary key)
            user = User.objects.get(username=username, is_approved=False, is_regular=True)
            user.is_approved = True
            user.budget = float(budget)  # Ensure budget is saved as a float/decimal
            user.save()  # Save changes to the user
            messages.success(request, f"Regular user {user.username} approved and budget allocated.")
            return redirect('approve_user')  # Redirect to a success page
        except User.DoesNotExist:
            messages.error(request, "User does not exist or is already approved.")
            
            

    # Update the context to include additional data
    context = {
        'tracker': tracker,
        'title': 'BUDGET APPROVAL',
        'CAMPUS_NAME': CAMPUS_NAME,
        'users': unapproved_users  # Pass unapproved users to the context
    }

    return render(request, 'accounts/Admin/Budget_Officer/bobudget.html', context)



def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        
        user = authenticate(request, username=username, password=pass1)
        
        if user is not None:
            # Check if the user's account is approved
            if user.is_approved:
                auth_login(request, user)
                
                # Redirect based on user_type
                if user.user_type == 'admin':
                    return redirect('user') 
                elif user.user_type == 'cd':
                    return redirect('cdlanding')
                elif user.user_type == 'budget':
                    return redirect('budget-landing')
                elif user.user_type == 'bac':
                    return redirect('baclanding')
                else: 
                    return redirect('ppmp101')  # Regular user
                
            else:
                messages.error(request, "Your account is not approved yet. Please wait for admin approval.")
                return redirect('login')
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
    
    return render(request, 'accounts/User/login.html')



@authenticated_user
def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out.")
    return redirect('login')



def bac(request):
    return render(request, 'accounts/User/bac.html')



@bac_required
def bac_request(request):

    tracker = Pr_identifier.objects.select_related('user').all()
    context = {
        'tracker': tracker,
        'title': 'PURCHASE REQUESTS',
        'CAMPUS_NAME': CAMPUS_NAME,
  
    }
        
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_request.html', context)


def ppmpform(request, year, pr_id):
 
    
    approved_checkouts = Checkout.objects.filter(bo_status='approved', cd_status='approved', user=request.user, year=year, pr_id=pr_id)


    approved_items = CheckoutItems.objects.filter(checkout__in=approved_checkouts)


    context = {
        'approved_items': approved_items,
        'year': year,
        'pr_id': pr_id,
        'bac_status': approved_checkouts.first().bac_status,
        'bo_comment': approved_checkouts.first().bo_comment,
        'cd_comment': approved_checkouts.first().cd_comment, 
        'SITE_TITLE' : SITE_TITLE,
        'CAMPUS_NAME' : CAMPUS_NAME,
        'title': 'APPROVED PPMP',
    }
   

    return render(request, 'accounts/User/myppmp.html', context)


def landing(request):
    return render(request, 'accounts/User/landing.html')

@authenticated_user
def about(request):
    context = {
    'title':'CTU-AC SUPPLY OFFICE REQUEST MONITORING SYSTEM',
    'CAMPUS_NAME': CAMPUS_NAME,
    }

    return render(request, 'accounts/User/about.html', context)



@authenticated_user
def tracker(request):
    checkouts = Checkout.objects.filter(user=request.user)
  

    checkout_data = []

    for checkout in checkouts:
        checkout_dict = {
            'submission_date': checkout.submission_date,
            'user': checkout.user,
            'pr_id': checkout.pr_id,
            'last_updated': checkout.last_updated,
            'cd_status': checkout.cd_status,  
            'cd_comment': checkout.cd_comment,
            'bo_status': checkout.bo_status,
            'bo_comment': checkout.bo_comment
            
        }
        checkout_data.append(checkout_dict)

    context = {
        'checkouts': checkout_data,
        'user': request.user,
        'title': "PPMP REQUEST STATUS",
        'CAMPUS_NAME': CAMPUS_NAME,
        
        
    }
    return render(request, 'accounts/User/tracker.html', context)

@authenticated_user
def prof(request):
    return render(request, 'accounts/User/prof.html')


@authenticated_user
def profile(request):
    return render(request, 'accounts/User/profile.html')

@bac_required
def bac_about(request):
    context = {
        'title': 'CTU-AC SUPPLY OFFICE REQUEST MONITORING SYSTEM',
        'CAMPUS_NAME': CAMPUS_NAME,
    }
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_about.html', context)



from django.shortcuts import render, get_object_or_404, redirect
from .models import Pr_identifier, PR

from django.shortcuts import get_object_or_404, redirect, render
from .models import Pr_identifier, PR

def cdpurchase_approval(request, pr_id):
    if request.method == 'POST':
        # Get the new status and comment from the POST data
        new_status = request.POST.get('new_status')
        comment_content = request.POST.get('comment_content')
        
        item = request.POST.get('item')
        item_brand = request.POST.get('item_brand')
        unit = request.POST.get('unit')
        price = request.POST.get('price')

        # Get the PR identifier based on the pr_id
        checkout = Pr_identifier.objects.get(pr_id=pr_id)

        # Update the PR object related to the current Pr_identifier
        PR.objects.filter(pr_identifier=checkout).update(
            item=item,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price,
        )

        # Update the Pr_identifier with the new status and comment
        Pr_identifier.objects.filter(pr_id=pr_id).update(
            cd_status=new_status,
            cd_comment=comment_content
        )

        return redirect('cdpurchase')
    
    elif request.method == 'GET':
        # Retrieve the Pr_identifier and PR objects
        checkouts = get_object_or_404(Pr_identifier, pr_id=pr_id)
        checkout_items = PR.objects.filter(pr_identifier=checkouts)
        
        # Add comment content to context, if it exists
        comment_content = checkouts.cd_comment  # Get the comment content

        context = {
            'checkout': checkouts,
            'checkout_items': checkout_items,
            'user': request.user,
            'pr_id': pr_id,
            'status': checkouts.cd_status,
            'comment_content': comment_content,  # Add the comment to the context
            'title': 'PURCHASE REQUEST FOR APPROVAL',
            'CAMPUS_NAME': CAMPUS_NAME,
        }

        return render(request, 'accounts/Admin/Campus_Director/cdpurchase_approval.html', context)

 
def purchase_cd(request, pr_id):
    pr_identifier = get_object_or_404(Pr_identifier, pr_id=pr_id)
    checkout_items = PR.objects.filter(pr_identifier__pr_id=pr_id)
    context = {
        'checkout_items': checkout_items,
        'pr_id': pr_id,
        'purpose': pr_identifier.purpose,
    }
    return render(request, 'accounts/Admin/Campus_Director/purchase_cd.html', context)


def purchase_cd(request, pr_id):
    pr_identifier = get_object_or_404(Pr_identifier, pr_id=pr_id)
    
    checkout_items = PR.objects.filter(pr_identifier__pr_id=pr_id)
    
    context = {
        'checkout_items': checkout_items,
        'pr_id': pr_id,
        'purpose': pr_identifier.purpose,
        
    }
   
    return render(request, 'accounts/Admin/Campus_Director/purchase_cd.html', context)

@bac_required
def bac_home(request):
    checkouts = Checkout.objects.select_related('user').all()
  

    checkout_data = []

    for checkout in checkouts:
        checkout_dict = {
            'submission_date': checkout.submission_date,
            'user': checkout.user,
            'pr_id': checkout.pr_id,
            'last_updated': checkout.last_updated,
            'cd_status': checkout.cd_status,  
            'cd_comment': checkout.cd_comment,
            'bo_status': checkout.bo_status,
            'bo_comment': checkout.bo_comment
            
        }
        checkout_data.append(checkout_dict)

    context = {
        'checkouts': checkout_data,
        'user': request.user,
        'title':'PPMP OF THE USERS',
        'CAMPUS_NAME' : CAMPUS_NAME,
    }

    return render(request, 'accounts/Admin/BAC_Secretariat/bac_home.html', context)

def bac_purchaserequest(request, pr_id):
    checkouts = get_object_or_404(Pr_identifier, pr_id=pr_id)
    checkout_items = PR.objects.filter(pr_identifier=checkouts)
    context = {
        'checkout': checkouts,
        'checkout_items': checkout_items,
        'user': request.user,
        'pr_id': pr_id,
        'status': checkouts.status,
        'title': 'PURCHASE REQUEST ITEMS',
        'CAMPUS_NAME' : CAMPUS_NAME,
    }
        
    
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_purchaserequest.html', context)

@bac_required
def bac_ppmp(request, pr_id):
    checkouts = get_object_or_404(Checkout, pr_id=pr_id)
    checkout_items = CheckoutItems.objects.filter(checkout=checkouts)
    context = {
            
            'checkout_items': checkout_items,
            'pr_id': pr_id,
            'title': 'PPMP REQUEST',
            'CAMPUS_NAME': CAMPUS_NAME,
    }

    if request.method == 'POST':
        
        comment_content = request.POST.get('comment_content')

        item = request.POST.get('item')
        item_brand = request.POST.get('item_brand')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        estimate = request.POST.get('estimate_budget')
        jan = request.POST.get('jan')
        feb = request.POST.get('feb')
        mar = request.POST.get('mar')
        apr = request.POST.get('apr')
        may = request.POST.get('may')
        jun = request.POST.get('jun')
        jul = request.POST.get('jul')
        aug = request.POST.get('aug')
        sep = request.POST.get('sep')
        oct = request.POST.get('oct')
        nov = request.POST.get('nov')
        dec = request.POST.get('dec')

        checkout = Checkout.objects.get(pr_id=pr_id)

        CheckoutItems.objects.filter(checkout=checkout, item=item).update(
            item=item,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price,
            estimate_budget=estimate,
            jan=jan,
            feb=feb,
            mar=mar,
            apr=apr,
            may=may,
            jun=jun,
            jul=jul,
            aug=aug,
            sep=sep,
            oct=oct,   
            nov=nov,
            dec=dec,
            
        )

        # Update Checkout model
        Checkout.objects.filter(pr_id=pr_id).update(
            
            bac_status=comment_content
        )

        return redirect('bac_home')

    elif request.method == 'GET':

        checkouts = get_object_or_404(Checkout, pr_id=pr_id)
        checkout_items = CheckoutItems.objects.filter(checkout=checkouts)
        context = {
            'checkout': checkouts,
            'checkout_items': checkout_items,
            'user': request.user,
            'pr_id': pr_id,
            'title': 'PPMP REQUEST',
            'CAMPUS_NAME': CAMPUS_NAME,
     }
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_ppmp.html', context)

def preqform(request, pr_id):

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        comment = request.POST.get('comment_content')

        Pr_identifier.objects.filter(pr_id=pr_id).update(
            status=new_status,
            comment=comment
            
        )
        return redirect('bac_home')
    
    elif request.method == 'GET':
        pr_identifier = get_object_or_404(Pr_identifier, pr_id=pr_id)
        pr_items = PR.objects.filter(pr_identifier=pr_identifier)

        context = {
            'pr_identifier': pr_identifier,
            'pr_items': pr_items,
            'user_first_name': request.user.first_name,
            'user_last_name': request.user.last_name,
            'user': request.user,
        }

    return render(request, 'accounts/Admin/Budget_Officer/borequest.html', context)



@authenticated_user
def np(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/np.html')

@bac_required
@authenticated_user
def purchaseorder(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/purchaseorder.html')


@authenticated_user
def bids(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bids.html')


@authenticated_user
def noa(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/noa.html')




@authenticated_user
def inspection(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/inspection.html')


@authenticated_user
def property(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/property.html')



@authenticated_user
def notif(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/notif.html')


@authenticated_user
def abstract(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/abstract.html')
@bac_required
@authenticated_user
def bac_prof(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_prof.html')
@bac_required
@authenticated_user
def bac_profile(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_profile.html')
@budget_required
@authenticated_user
def bo(request):
    return render(request, 'accounts/Admin/Budget_Officer/bo.html')

@budget_required
@authenticated_user
def boabout(request):
    context = {
    'title': 'CTU-AC SUPPLY OFFICE REQUEST MONITORING SYSTEM',
    'CAMPUS_NAME': CAMPUS_NAME,
    }
    return render(request, 'accounts/Admin/Budget_Officer/boabout.html', context)



@budget_required
@authenticated_user

@cd_required
@authenticated_user
def cd(request):
    return render(request, 'accounts/Admin/Campus_Director/cd.html')

@cd_required
@authenticated_user
def cdabout(request):
    context = {
    'title': 'CTU-AC SUPPLY OFFICE REQUEST MONITORING SYSTEM',
    'CAMPUS_NAME': CAMPUS_NAME,
    }
    return render(request, 'accounts/Admin/Campus_Director/cdabout.html', context)

@cd_required
@authenticated_user
def cdppmp(request):
    checkouts = Checkout.objects.select_related('user').all()
  

    checkout_data = []

    for checkout in checkouts:
        checkout_dict = {
            'submission_date': checkout.submission_date,
            'user': checkout.user,
            'pr_id': checkout.pr_id,
            'last_updated': checkout.last_updated,
            'cd_status': checkout.cd_status,  
            'cd_comment': checkout.cd_comment,
            'bo_status': checkout.bo_status,
            'bo_comment': checkout.bo_comment
        }
        checkout_data.append(checkout_dict)

    context = {
        'checkouts': checkout_data,
        'user': request.user,
        'title':'PPMP REQUEST',
        'CAMPUS_NAME': CAMPUS_NAME,   
    }
    return render(request, 'accounts/Admin/Campus_Director/cdppmp.html', context)

@cd_required
@authenticated_user
def cdresolution(request):
    context ={
        'title': 'RESOLUTION',
        'CAMPUS_NAME': CAMPUS_NAME,
    }
    return render(request, 'accounts/Admin/Campus_Director/cdresolution.html', context)


@authenticated_user
def resolution(request):
    return render(request, 'accounts/Admin/Campus_Director/resolution.html')


@admin_required
@authenticated_user
def admin_home(request):
    return render(request, 'accounts/Admin/System_Admin/admin_home.html')


@admin_required
@authenticated_user
def adminabout(request):
    return render(request, 'accounts/Admin/System_Admin/adminabout.html')

@admin_required
@authenticated_user
def user(request):
    users = User.objects.all()
    return render (request, 'accounts/Admin/System_Admin/user.html',{'users': users})

def requests(request):
    return render(request, 'accounts/Admin/System_Admin/requests.html')


   
def delete_user(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect('user')


@authenticated_user
def addItem(request):
    if request.method == 'POST':
        item_data = request.POST.get('item')
        item_brand_description = request.POST.get('item_Brand_Description')
        unit = request.POST.get('unit')
        unit_cost = request.POST.get('unit_Cost')


       
        user = request.user
        Item.objects.create(
            user=user,
            item=item_data,
            item_brand_description=item_brand_description,
            unit=unit,
            unit_cost=unit_cost,
        )

        return redirect('ppmp')
    
    return render(request, 'accounts/User/ppmp.html')


@authenticated_user
def catalogue (request):
    grouped_data = {}  # Define grouped_data outside of if conditions
    if request.method == 'POST':
        item_name = request.POST.get(f'item')
        item_brand = request.POST.get(f'item_brand')
        unit = request.POST.get(f'unit')
        price = request.POST.get(f'price')

        
        Item.objects.create(
            user=request.user,
            item=item_name,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price
        )

        return redirect('catalogue')

    elif request.method == 'GET':
        csv_data = CSV.objects.all().order_by('Category')
        for key, group in itertools.groupby(csv_data, key=lambda x: x.Category):
            grouped_data[key] = list(group)

    context = {
        'grouped_data' : grouped_data,
        'title' : 'CATALOGUE',
        'CAMPUS_NAME' : CAMPUS_NAME,
    }
    return render(request, 'accounts/User/catalogue.html', context)


@authenticated_user
def myppmp(request):
    
    approved_checkouts = Checkout.objects.filter(bo_status='approved', cd_status = 'approved')

   
    approved_items = CheckoutItems.objects.filter(checkout__in=approved_checkouts)

    context = {
        'approved_items': approved_items,
        'SITE_TITLE' : SITE_TITLE,
        'CAMPUS_NAME' : CAMPUS_NAME,
    }

    return render(request, 'accounts/User/myppmp.html', context)



@authenticated_user
def ppmp(request):    
    context = {
        'title' : 'CREATE PROJECT PROCUREMENT MANAGEMENT PLAN(PPMP)',
        'CAMPUS_NAME' : CAMPUS_NAME,
    }
    if request.method == 'POST':

        year = request.POST.get('selectedYear')
        
        new_checkout = Checkout.objects.create(
            user=request.user,
            year=year,
        )
        
        items = request.POST.getlist('item')
        
        item_brands = request.POST.getlist('item_brand')
        units = request.POST.getlist('unit')
        estimate_budgets = request.POST.getlist('estimate_budget')
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
        prices = request.POST.getlist('price')
        

        

        for i in range(len(items)):
            CheckoutItems.objects.create(
                checkout=new_checkout,
                item=items[i],
                item_brand_description=item_brands[i],
                unit=units[i],
                estimate_budget=estimate_budgets[i],
                jan=jans[i],
                feb=febs[i],
                mar=mars[i],
                apr=aprs[i],
                may=mays[i],
                jun=juns[i],
                jul=juls[i],
                aug=augs[i],
                sep=seps[i],
                oct=octs[i],
                nov=novs[i],
                dec=decs[i],
                unit_cost=prices[i]
            )

        pr_id = new_checkout.combined_id

        new_checkout.pr_id = pr_id
        new_checkout.save()

        # delete the items from the Item
        Item.objects.filter(user=request.user).delete()

        return redirect('tracker')
    elif request.method == 'GET':
    
        items = Item.objects.all()
        context['items'] = items
        
        return render(request, 'accounts/User/ppmp.html', context)




from django.core.files.base import ContentFile
@authenticated_user
def purchase(request):
    context = {
                'title': 'CREATE PURCHASE REQUEST',
                'CAMPUS_NAME': CAMPUS_NAME,
                }
    if request.method == 'POST':
        files = request.FILES.getlist('files[]')
        items = request.POST.getlist('items[]')
        item_brands = request.POST.getlist('item_brands[]')
        units = request.POST.getlist('units[]')
        prices = request.POST.getlist('prices[]')
        quantity = request.POST.getlist('quantity[]')
        total = request.POST.get('total_amount')

        pr_id = generate_auto_pr_id()
        user = request.user
        purpose = request.POST.get('purpose')
        pr_identifier = Pr_identifier.objects.create(user=user, pr_id=pr_id, purpose=purpose,)

        for i in range(len(items)):
            uploaded_file = files[i] if i < len(files) else None  
            metadata = FileMetadata.objects.create(filename=uploaded_file.name if uploaded_file else '')

            if uploaded_file:
                metadata.file.save(uploaded_file.name, ContentFile(uploaded_file.read()))

            PR.objects.create(
                metadata=metadata,
                file=metadata.file if uploaded_file else None, 
                pr_identifier=pr_identifier,
                item=items[i],
                item_brand_description=item_brands[i],
                unit=units[i],
                unit_cost=prices[i],
                quantity=quantity[i],
                total_cost=total
            )
            
            # Remove the following line, it is not necessary
            PR_Items.objects.all().delete()

        # Move the redirect statement outside the loop
        return redirect('purchasetracker')

    elif request.method == 'GET':
        items = PR_Items.objects.all()
        context['items'] = items  # Add 'items' to the context dictionary
        return render(request, 'accounts/User/purchase.html', context)


from bson import ObjectId

def generate_auto_pr_id():
    # Generate a unique pr_id using ObjectId
    pr_id = str(ObjectId())
    return pr_id


@authenticated_user
def approved_ppmp(request):
    if request.method == 'POST':
        item = request.POST.get('item')
        item_brand = request.POST.get('item_brand')
        unit = request.POST.get('unit')
        price = request.POST.get('unit_cost')

        PR_Items.objects.create(
            item=item,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price
 
        )

        return redirect('approved_ppmp')
    elif request.method == 'GET':
        try:
            # Get the latest approved checkout based on submission date
            latest_checkout = Checkout.objects.filter(bo_status='approved', cd_status='approved').order_by('-year').first()

            if latest_checkout:
                checkout_items = CheckoutItems.objects.filter(checkout=latest_checkout)
                latest_year = latest_checkout.year
            else:
                checkout_items = []
                latest_year = None

        except Checkout.DoesNotExist:
            checkout_items = []
            latest_year = None

        context = {
            'checkout_items': checkout_items,
            'latest_year': latest_year,
            'title': 'APPROVED PPMP',
            'CAMPUS_NAME': CAMPUS_NAME,
        }
        return render(request, 'accounts/User/approved_ppmp.html', context)

@authenticated_user
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})


@bac_required
def bac_history(request):
   request = Item.objects.all()
   return render(request,  'accounts/Admin/BAC_Secretariat/bac_history.html', {'request': request})

def add_new_item(request):
    if request.method == 'POST':
        category = request.POST.get('category')
        new_item_name = request.POST.get('new_item_name')
        new_item_brand = request.POST.get('new_item_brand')
        new_item_unit = request.POST.get('new_item_unit')
        new_item_price = request.POST.get('new_item_price')

        new_item = CSV(
            Category=category,
            Item_name=new_item_name,
            Item_Brand=new_item_brand,
            Unit=new_item_unit,
            Price=new_item_price,
        )

        new_item.save()
        return redirect('bac_dashboard')
    
def user_add_new_item(request):
    if request.method == 'POST':
        
        new_item_name = request.POST.get('new_item_name')
        new_item_brand = request.POST.get('new_item_brand')
        new_item_unit = request.POST.get('new_item_unit')
        new_item_price = request.POST.get('item_unit_price')
        

        new_item = Item(
            item=new_item_name,
            item_brand_description=new_item_brand,
            unit=new_item_unit,
            unit_cost=new_item_price,
            
        )

        new_item.save()
        return redirect('ppmp')



@bac_required
def bac_dashboard(request):
    if request.method == 'GET':
        csv_data = CSV.objects.all().order_by('Category')
        grouped_data = {}
        for key, group in itertools.groupby(csv_data, key=lambda x: x.Category):
            grouped_data[key] = list(group)

        context = {
            'grouped_data': grouped_data,
            'title': 'AVIALABLE ITEMS',
            'CAMPUS_NAME': CAMPUS_NAME,
        }
        
        return render(request, 'accounts/Admin/BAC_Secretariat/bac_dashboard.html', context)

    elif request.method == 'POST':
        new_category = request.POST.get('custom-category', '').strip()
        if new_category:
            CSV.objects.create(Category=new_category)

        return redirect('bac_dashboard')


def upload_file(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')
        if uploaded_file:
            handle_uploaded_file(uploaded_file)
            return redirect('bac_dashboard')  
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_dashboard.html')


def handle_uploaded_file(file):
    decoded_file = file.read().decode('utf-8')
    csv_data = csv.reader(decoded_file.splitlines(), delimiter=',')
    next(csv_data)
    for row in csv_data:
        CSV.objects.create(
            Category=row[0],
            Item_name=row[1],
            Item_Brand=row[2],
            Unit=row[3],   
            Price=row[4]
        )

def delete_item(request, id):
    item = CSV.objects.get(id=id)
    item.delete()
    return redirect('bac_dashboard')



def delete(request, id):
     item = Item.objects.get(id=id)
     item.delete()
     return redirect('ppmp')


def update_item(request, id):
    if request.method == 'POST':
        CSV.objects.get(id=id)
        
        item_name = request.POST.get(f'item_{id}')
        item_brand = request.POST.get(f'item_brand_{id}')
        unit = request.POST.get(f'unit_{id}')
        price = request.POST.get(f'price_{id}')
    
        CSV.objects.filter(id=id).update(
            Item_name=item_name,
            Item_Brand=item_brand,
            Unit=unit,
            Price=price
        )
        
        return redirect('bac_dashboard')

def update(request, id):
    if request.method == 'POST':
        Item.objects.get(id=id)
        
        
        item_name = request.POST.get(f'item_{id}')
        
        item_brand = request.POST.get(f'item_brand_{id}')
       
        unit = request.POST.get(f'unit_{id}')
        
        
        price = request.POST.get(f'price_{id}')
        

        Item.objects.filter(id=id).update(
           item=item_name,
           item_brand_description=item_brand,
           unit=unit,
           unit_cost=price
        )
        
        return redirect('ppmp')

def delete_category(request, Category):
    items_to_delete = CSV.objects.filter(Category=Category)
    items_to_delete.delete()
    return redirect('bac_dashboard')


@budget_required
def bohome(request):
    checkouts = Checkout.objects.select_related('user').all()
  
    checkout_data = []

    for checkout in checkouts:
        checkout_dict = {
            'submission_date': checkout.submission_date,
            'user': checkout.user,
            'pr_id': checkout.pr_id,
            'last_updated': checkout.last_updated,
            'bo_status': checkout.bo_status,  
            'bo_comment': checkout.bo_comment,
            'cd_status': checkout.cd_status,  
            'cd_comment': checkout.cd_comment,
        }
        checkout_data.append(checkout_dict)

    context = {
        'checkouts': checkout_data,
        'title': 'PPMP REQUEST',
        'CAMPUS_NAME':CAMPUS_NAME,
    }

    return render(request, 'accounts/Admin/Budget_Officer/bohome.html', context)



def preqform_bo(request, pr_id):

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
 
        comment_content = request.POST.get('comment_content')


        item = request.POST.get('item')
        item_brand = request.POST.get('item_brand')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        estimate = request.POST.get('estimate_budget')
        jan = request.POST.get('jan')
        feb = request.POST.get('feb')
        mar = request.POST.get('mar')
        apr = request.POST.get('apr')
        may = request.POST.get('may')
        jun = request.POST.get('jun')
        jul = request.POST.get('jul')
        aug = request.POST.get('aug')
        sep = request.POST.get('sep')
        oct = request.POST.get('oct')
        nov = request.POST.get('nov')
        dec = request.POST.get('dec')

        checkout = Checkout.objects.get(pr_id=pr_id)    

        CheckoutItems.objects.filter(checkout=checkout, item=item).update(
            item=item,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price,
            estimate_budget=estimate,
            jan=jan,
            feb=feb,
            mar=mar,
            apr=apr,
            may=may,
            jun=jun,
            jul=jul,
            aug=aug,
            sep=sep,
            oct=oct,
            nov=nov,
            dec=dec,
            
        )
        Checkout.objects.filter(pr_id=pr_id).update(
            bo_status=new_status,
            bo_comment=comment_content,
            bo_approved_date = timezone.now() 
        )

        return redirect('bohome')
       
    elif request.method == 'GET':
        checkouts = get_object_or_404(Checkout, pr_id=pr_id)
        checkout_item = CheckoutItems.objects.filter(checkout=checkouts)
        context = {
            'checkouts': checkouts,
            'checkout_item': checkout_item,
            'pr_id': pr_id,
            'title': 'PPMP REQUEST FOR APPROVAL',
            'CAMPUS_NAME': CAMPUS_NAME,
        }
        
        return render(request, 'accounts/Admin/Budget_Officer/preqform_bo.html', context)

        

def cdppmp_approval(request, pr_id):
    if request.method == 'POST':
        # Get the form data from the POST request
        new_status = request.POST.get('new_status')
        comment_content = request.POST.get('comment_content')
        # Item details
        item = request.POST.get('item')
        item_brand = request.POST.get('item_brand')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        estimate = request.POST.get('estimate_budget')
        jan = request.POST.get('jan')
        feb = request.POST.get('feb')
        mar = request.POST.get('mar')
        apr = request.POST.get('apr')
        may = request.POST.get('may')
        jun = request.POST.get('jun')
        jul = request.POST.get('jul')
        aug = request.POST.get('aug')
        sep = request.POST.get('sep')
        oct = request.POST.get('oct')
        nov = request.POST.get('nov')
        dec = request.POST.get('dec')

        # Get the Checkout object using pr_id
        checkout = Checkout.objects.get(pr_id=pr_id)

        # Update the CheckoutItems related to the specific checkout and item
        CheckoutItems.objects.filter(checkout=checkout, item=item).update(
            item=item,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price,
            estimate_budget=estimate,
            jan=jan,
            feb=feb,
            mar=mar,
            apr=apr,
            may=may,
            jun=jun,
            jul=jul,
            aug=aug,
            sep=sep,
            oct=oct,
            nov=nov,
            dec=dec,
        )

        # Update the Checkout model with the new status and comments
        Checkout.objects.filter(pr_id=pr_id).update(
            cd_status=new_status,
            cd_comment=comment_content,
            cd_approved_date=timezone.now()
        )

        # Redirect to the CD PPMP page after approval
        return redirect('cdppmp')

    elif request.method == 'GET':
        # Get the checkout object and related items
        checkouts = get_object_or_404(Checkout, pr_id=pr_id)
        checkout_items = CheckoutItems.objects.filter(checkout=checkouts)

        # Prepare the context for rendering the page
        context = {
            'checkout': checkouts,
            'checkout_items': checkout_items,
            'user': request.user,
            'pr_id': pr_id,
            'title': 'PPMP REQUEST APPROVAL',
            'CAMPUS_NAME': CAMPUS_NAME,  # Ensure CAMPUS_NAME is defined somewhere in the view
        }

        return render(request, 'accounts/Admin/Campus_Director/cdppmp_approval.html', context)
@cd_required
def cdpurchase(request):

    checkouts = Pr_identifier.objects.select_related('user').all()
  

    checkout_data = []

    for checkout in checkouts:
        checkout_dict = {
            'submission_date': checkout.submission_date,
            'user': checkout.user,
            'pr_id': checkout.pr_id,
            'cd_status': checkout.cd_status,  
            'cd_comment': checkout.cd_comment,
            'bo_status': checkout.bo_status,
            'bo_comment': checkout.bo_comment
            
            
           
        }
        checkout_data.append(checkout_dict)

    context = {
        'checkouts': checkout_data,
        'user': request.user,
        'title': 'PURCHASE REQUESTS',
        'CAMPUS_NAME': CAMPUS_NAME,     
    }

   

    return render(request, 'accounts/Admin/Campus_Director/cdpurchase.html', context)

def preqform_cd(request, pr_id):
    # Fetch the Checkout object based on the pr_id
    checkout = get_object_or_404(Checkout, pr_id=pr_id)
    
    if request.method == 'POST':
        # Handle POST data as before
        new_status = request.POST.get('new_status')
        comment_content = request.POST.get('comment_content')

        item = request.POST.get('item')
        item_brand = request.POST.get('item_brand')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        estimate = request.POST.get('estimate_budget')
        jan = request.POST.get('jan')
        feb = request.POST.get('feb')
        mar = request.POST.get('mar')
        apr = request.POST.get('apr')
        may = request.POST.get('may')
        jun = request.POST.get('jun')
        jul = request.POST.get('jul')
        aug = request.POST.get('aug')
        sep = request.POST.get('sep')
        oct = request.POST.get('oct')
        nov = request.POST.get('nov')
        dec = request.POST.get('dec')

        # Update the CheckoutItems
        CheckoutItems.objects.filter(checkout=checkout, item=item).update(
            item=item,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price,
            estimate_budget=estimate,
            jan=jan,
            feb=feb,
            mar=mar,
            apr=apr,
            may=may,
            jun=jun,
            jul=jul,
            aug=aug,
            sep=sep,
            oct=oct,
            nov=nov,
            dec=dec,
        )

        # Update the Checkout object
        checkout.cd_status = new_status
        checkout.cd_comment = comment_content
        checkout.cd_approved_date = timezone.now()
        checkout.save()

        return redirect('cdpurchase')

    else:  # GET request
        checkout_items = CheckoutItems.objects.filter(checkout=checkout)
        context = {
            'checkouts': checkout,
            'checkout_items': checkout_items,
            'pr_id': pr_id,
        }
        return render(request, 'accounts/Admin/Campus_Director/preqform_cd.html', context)

@authenticated_user              
def delete_items(request, id):
    item = Item.objects.get(id = id)
    item.delete()
    return redirect ('requester')

def checkout_items_view(request):
    checkout_items = CheckoutItems.objects.all()
    context = {'checkout_items': checkout_items}
    return render(request, 'attachment/checkout_items.html', context)


@authenticated_user
def purchasetracker(request):
    tracker = Pr_identifier.objects.filter(user=request.user).order_by('-submission_date')
    context = {
        'tracker': tracker,
        'title': 'PURCHASE REQUEST TRACKER',
        'CAMPUS_NAME': CAMPUS_NAME,
    }


    return render(request, 'accounts/User/purchasetracker.html', context)



def boppmp(request, pr_id):

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        comment_content = request.POST.get('comment_content')

        item = request.POST.get('item')
        item_brand = request.POST.get('item_brand')
        unit = request.POST.get('unit')
        price = request.POST.get('price')
        estimate = request.POST.get('estimate_budget')
        jan = request.POST.get('jan')
        feb = request.POST.get('feb')
        mar = request.POST.get('mar')
        apr = request.POST.get('apr')
        may = request.POST.get('may')
        jun = request.POST.get('jun')
        jul = request.POST.get('jul')
        aug = request.POST.get('aug')
        sep = request.POST.get('sep')
        oct = request.POST.get('oct')
        nov = request.POST.get('nov')
        dec = request.POST.get('dec')

        checkout = Checkout.objects.get(pr_id=pr_id)

        CheckoutItems.objects.filter(checkout=checkout, item=item).update(
            item=item,
            item_brand_description=item_brand,
            unit=unit,
            unit_cost=price,
            estimate_budget=estimate,
            jan=jan,
            feb=feb,
            mar=mar,
            apr=apr,
            may=may,
            jun=jun,
            jul=jul,
            aug=aug,
            sep=sep,
            oct=oct,   
            nov=nov,
            dec=dec,
            
        )

        # Update Checkout model
        Checkout.objects.filter(pr_id=pr_id).update(
            bo_status=new_status,
            bo_comment=comment_content,
            bo_approved_date = timezone.now()
        )

        return redirect('bohome')

    elif request.method == 'GET':
        checkouts = get_object_or_404(Checkout, pr_id=pr_id)
        checkout_items = CheckoutItems.objects.filter(checkout=checkouts)
        context = {
            'checkout': checkouts,
            'checkout_items': checkout_items,
            'user': request.user,
            'pr_id': pr_id,
     }

    return render(request, 'accounts/Admin/Budget_Officer/boppmp.html', context)

def new_ppmp(request):
    return render(request, 'accounts/User/new_ppmp.html')






def get_tracker_updates(request):
    updates = []
    checkouts = Checkout.objects.all()

    for checkout in checkouts:
        update = {
            'pr_id': checkout.pr_id,
            'bo_status': checkout.bo_status,  # Business Office status
            'bo_comment': checkout.bo_comment or 'No comment',
            'cd_status': checkout.cd_status,  # CD status
            'cd_comment': checkout.cd_comment or 'No comment',  # CD comment
        }
        updates.append(update)

    return JsonResponse(updates, safe=False)


def checkout_action(request, checkout_id):
    # Get the specific checkout item
    checkout = get_object_or_404(Checkout, id=checkout_id)

    # Action could be 'approve' or 'disapprove' for Business Office or Purchasing
    action = request.POST.get('action')
    comment = request.POST.get('comment', '')

    # Check whether the action is for Business Office or Purchasing
    status_type = request.POST.get('status_type')  # 'bo' for Business Office or 'cd' for Purchasing

    # Initialize message and update the status
    if status_type == 'bo':
        if action == 'approve':
            checkout.bo_status = 'approved'
            message = f'PPMP No. {checkout.pr_id} has been approved by Business Office.'
        elif action == 'disapprove':
            checkout.bo_status = 'disapproved'
            message = f'PPMP No. {checkout.pr_id} has been disapproved by Business Office.'
        else:
            return JsonResponse({'error': 'Invalid action for BO'}, status=400)

        # Update the comment if provided
        if action == 'disapprove':
            checkout.bo_comment = comment or 'No additional comments provided.'

    elif status_type == 'cd':
        if action == 'approve':
            checkout.cd_status = 'approved'
            message = f'PPMP No. {checkout.pr_id} has been approved by Purchasing.'
        elif action == 'disapprove':
            checkout.cd_status = 'disapproved'
            message = f'PPMP No. {checkout.pr_id} has been disapproved by Purchasing.'
        else:
            return JsonResponse({'error': 'Invalid action for CD'}, status=400)

        # Update the comment if provided
        if action == 'disapprove':
            checkout.cd_comment = comment or 'No additional comments provided.'

    else:
        return JsonResponse({'error': 'Invalid status type'}, status=400)

    # Save the updated status and comment
    checkout.save()

    # Prepare the notification message
    notification = {
        'pr_id': checkout.pr_id,
        'message': message,
        'comment': checkout.bo_comment if status_type == 'bo' else checkout.cd_comment,
    }

    # Return the notification as part of the response
    return JsonResponse(notification)



def get_purchasetracker_updates(request):
    updates = []
    tracker = Pr_identifier.objects.filter(user=request.user).order_by('-submission_date')

    for pr in tracker:
        update = {
            'pr_id': pr.pr_id,
            'bo_status': pr.bo_status,  # Business Office status
            'bo_comment': pr.bo_comment or 'No comment',
            'cd_status': pr.cd_status,  # CD status
            'cd_comment': pr.cd_comment or 'No comment',  # CD comment
        }
        updates.append(update)

    return JsonResponse(updates, safe=False)


def tracker_action(request, pr_id):  # Use pr_id instead of checkout_id
    # Get the specific purchase request tracker item
    tracker = get_object_or_404(Pr_identifier, pr_id=pr_id)

    # Get the action (approve/disapprove) and comment from the POST request
    action = request.POST.get('action')
    comment = request.POST.get('comment', '')

    # Get the status type (either 'bo' for Business Office or 'cd' for Purchasing)
    status_type = request.POST.get('status_type')

    # Initialize message and update the status based on status_type
    if status_type == 'bo':
        if action == 'approve':
            tracker.bo_status = 'approved'
            message = f'pr_id {tracker.pr_id} has been approved by Business Office.'
        elif action == 'disapprove':
            tracker.bo_status = 'disapproved'
            message = f'pr_id {tracker.pr_id} has been disapproved by Business Office.'
        else:
            return JsonResponse({'error': 'Invalid action for BO'}, status=400)

        # Update the comment if disapproved
        if action == 'disapprove':
            tracker.bo_comment = comment or 'No additional comments provided.'

    elif status_type == 'cd':
        if action == 'approve':
            tracker.cd_status = 'approved'
            message = f'pr_id {tracker.pr_id} has been approved by Purchasing.'
        elif action == 'disapprove':
            tracker.cd_status = 'disapproved'
            message = f'pr_id {tracker.pr_id} has been disapproved by Purchasing.'
        else:
            return JsonResponse({'error': 'Invalid action for CD'}, status=400)

        # Update the comment if disapproved
        if action == 'disapprove':
            tracker.cd_comment = comment or 'No additional comments provided.'

    else:
        return JsonResponse({'error': 'Invalid status type'}, status=400)

    # Save the updated status and comment
    tracker.save()

    # Prepare the notification message
    notification = {
        'pr_id': tracker.pr_id,
        'message': message,
        'comment': tracker.bo_comment if status_type == 'bo' else tracker.cd_comment,
    }

    # Return the notification as part of the response
    return JsonResponse(notification)

def sidebar1(request):
    return render(request, 'accounts/User/sidebar1.html')