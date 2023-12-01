from audioop import reverse
import json
from django.http import HttpResponseRedirect, JsonResponse
from typing import ItemsView
from django.shortcuts import redirect, render, get_object_or_404
from django.core.cache import cache
from .models import *
import csv
from django.contrib.auth import authenticate, login as auth_login, logout
from .decorators import unauthenticated_user, authenticated_user
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
from .models import Item
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random


def main(request):
    return render(request, 'accounts/User/main.html')


def bac(request):
    return render(request, 'accounts/User/bac.html')


def homepage(request):
    return render(request, 'accounts/User/homepage.html')



def register(request):
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check if passwords match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/User/register.html')

        # Check if the username or email is already in use
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email is already in use.")
            return render(request, 'accounts/User/register.html')

        # Create a new user account
        user = User.objects.create_user(username=username, email=email, password=pass1, is_active=False)
        user.first_name = fname
        user.last_name = lname
        user.save()

        # Send an activation email
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

        messages.success(request, "Your account has been successfully created. Check your email for activation instructions.")
        return redirect('login')  # Redirect to the login page upon successful registration
    return render(request, 'accounts/User/register.html')


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



def login(request):
    if request.method == "POST":
        print('fddzjkfds')
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')  # Use 'pass1' as the password field name
        
        # Authenticate the user
        user = authenticate(request, username=username, password=pass1)
        if user is not None and user.is_active:
    # User is valid and active, log them in
           auth_login(request, user)
           messages.success(request, "You are now logged in.")
           return redirect('request')
        else:
            # Authentication failed, show an error message
            messages.error(request, "Invalid login credentials. Please try again.")
    return render(request, 'accounts/User/login.html')


def get_random_string(length, allowed_chars='0123456789'):
    return ''.join(random.choice(allowed_chars) for _ in range(length))



def handle_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        # Generate a random 4-digit verification code
        verification_code = get_random_string(4, '0123456789')
        
        # Store the verification code in the cache
        cache_key = f'verification_code_{email}'
        cache.set(cache_key, verification_code, 600)  # Store for 10 minutes (adjust as needed)
        
        # Send the verification code to the user's email
        subject = 'Password Reset Verification Code'
        message = f'Your verification code is: {verification_code}'
        from_email = 'rlphtzn@gmail.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        
        # Redirect the user to a page where they can enter the verification code
        return redirect('verify_code')  # Make sure 'verify_code' is a valid URL pattern
    return render(request, 'accounts/User/forgot.html')



def verify_code(request):
    if request.method == 'POST':
        code1 = request.POST.get('code1')
        code2 = request.POST.get('code2')
        code3 = request.POST.get('code3')
        code4 = request.POST.get('code4')

        verification_code = f"{code1}{code2}{code3}{code4}"
        user_email = request.POST.get('email')
        print('dsfsdfsdfdsfds')
        if is_valid_code(verification_code, user_email):
            return redirect('reset_password')  # Make sure 'reset_password' is a valid URL pattern
    return render(request, 'accounts/User/verify.html')  # Make sure the template exists


def is_valid_code(verification_code, user_email):
    # Construct the cache key based on the user's email
    cache_key = f'verification_code_{user_email}'
    
    # Retrieve the stored verification code from the cache
    stored_code = cache.get(cache_key)
    
    if stored_code and verification_code == stored_code:
        # Codes match, and the code exists in the cache
        return True
    return False



 # You can use this decorator to ensure the user is logged in to reset their password
def reset_password(request):
    if request.method == 'POST':
        # Handle the password reset form submission here
        new_password = request.POST.get('new_password')  # Assuming you have a form field with name="new_password"
        
        # Update the user's password securely
        user = request.user  # Get the current logged-in user
        
        # Set the new password for the user
        user.set_password(new_password)
        
        # Save the user to update the password in the database
        user.save()
        
        # To maintain the user's session after changing the password, you can use the following:
        update_session_auth_hash(request, user)
        
        # Redirect the user to a success page or login page
        messages.success(request, 'Password updated successfully.')
        return redirect('login')  # Change 'login' to the name of your login URL pattern
    return render(request, 'accounts/User/reset.html')  # Adjust the template name as needed


def logout_user(request):
    logout(request)
    messages.success(request, ("You are now successfully logout."))
    return redirect('homepage')


def about(request):
    return render(request, 'accounts/User/about.html')


def history(request):
    items = Item.objects.all()  # Fetch all Item instances from the database
    return render(request, 'accounts/User/history.html', {'items': items})


def tracker(request):
    # purchase_requests = PurchaseRequest.objects.all()
    # data = [{'purchase_request_id': request.ppurchase_request_id, 'status': request.status} for request in purchase_requests]
    return render(request, 'accounts/User/tracker.html')


def prof(request):
    return render(request, 'accounts/User/prof.html')


def profile(request):
    return render(request, 'accounts/User/profile.html')


def bac_about(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_about.html')


def bac_history(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_history.html')


def bac_home(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_home.html')


def preqform(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/preqform.html')


def np(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/np.html')


def bids(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bids.html')


def noa(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/noa.html')


def preqform(request):
    items = Item.objects.all()  # Fetch all Item instances from the database
    return render(request, 'accounts/Admin/BAC_Secretariat/preqform.html', {'items': items})


def purchaseorder(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/purchaseorder.html')


def inspection(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/inspection.html')


def property(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/property.html')


def np(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/np.html')

def notif(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/notif.html')
def abstract(request):
    # Your view logic here
    return render(request, 'accounts/Admin/BAC_Secretariat/abstract.html')
def profile_html(request):
    return render(request, 'profile.html')


def signout(request):
    pass



def addItem(request):
    if request.method == 'POST':
        item_data = request.POST.get('item')
        item_brand_description = request.POST.get('item_Brand_Description')
        unit = request.POST.get('unit')
        unit_cost = request.POST.get('unit_Cost')
        quantity = request.POST.get('quantity')

    
        Item.objects.create(
            item=item_data,
            item_brand_description=item_brand_description,
            unit=unit,
            unit_cost=unit_cost,
            quantity=quantity,
        )

        return redirect('requester')

    return render(request, 'accounts/User/request.html')


def request(request):
    if request.method == 'POST':
        # Retrieve selected rows from the form
        selected_rows = request.POST.getlist('selectRow')

        # Process and save data to the database
        for row_id in selected_rows:
            item_name = request.POST.get(f'item_{row_id}')
            item_brand = request.POST.get(f'item_brand_{row_id}')
            unit = request.POST.get(f'unit_{row_id}')
            price = request.POST.get(f'price_{row_id}')
            quantity = request.POST.get(f'quantity_{row_id}')

            # Save the data to the CartItem model (update this based on your model)
            items = Item.objects.create(
                item=item_name,
                item_brand_description=item_brand,
                unit=unit,
                unit_cost=price,
                quantity=quantity,
            )
            items.save()

        # Redirect to a success page
        return redirect('requester')

    else:
        # Handle data fetching for GET request
        # Connect to MongoDB
        csv_file_path = 'C:/Users/dugaduga.jhake/Desktop/SUPPLY SYSTEM/ONLINE_SUPPLY_OFFICE_COPY/items.csv'

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)
        
        # Pass data to the template
        return render(request, 'accounts/User/request.html', {'csv_data': csv_data})


def requester(request):
    items = Item.objects.all() 
    return render(request, 'accounts/User/cart.html', {'items': items})


def delete_item(request, item_id):
    try:
        item = get_object_or_404(Item, id=item_id)
        item.delete()
        message = f"{item_id} will be deleted."
        status = "success"
    except Exception as e:
        message = f"Error deleting item: {str(e)}"
        status = "error"

    return JsonResponse({"status": status, "message": message})






def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})



def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})


def item_delete(request, request_id):
    item = get_object_or_404(Item, request_id=request_id)
    item.delete()
    # Redirect to an appropriate URL after deletion
    return redirect('requester')  # Replace 'requester' with your desired redirect URL name
def your_view(request):
    # Replace this with your actual logic to retrieve items from the database
    items = Item.objects.all()

    # Calculate total cost for each item
    for item in items:
        item.total_cost = item.unit_cost * item.quantity

    return render(request, 'cart.html', {'items': items})

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PurchaseRequest, History

def get_additional_details(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        request = get_object_or_404(PurchaseRequest, request_id=request_id)
        
        # Placeholder for additional details retrieval logic
        additional_details = "Some additional details for request {}".format(request_id)
        
        return JsonResponse({"request_id": request_id, "additional_details": additional_details})

    return JsonResponse({"error": "Invalid request method"}, status=400)

def get_bac_history_data(request):
    # Placeholder for the actual logic to retrieve history data
    # For now, let's return some sample data
    history_data = [
        {"request_id": 1, "action": "Status updated", "timestamp": "2023-01-01 12:00:00"},
        {"request_id": 2, "action": "Status updated", "timestamp": "2023-01-02 14:30:00"},
        # Add more data as needed
    ]
    return JsonResponse(history_data, safe=False)

def update_status(request, id):
    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST)
        if form.is_valid():
            request_id = form.cleaned_data['id']
            status = form.cleaned_data['status']
            
            # Assuming you have a purchase request instance, you can update its status here
            # For demonstration purposes, let's create a new instance
            purchase_request = PurchaseRequest.objects.create(status=status)
             # Update the status
            purchase_request.update_status(status)

            return JsonResponse({'message': 'Purchase request status updated successfully.'})
        else:
            return JsonResponse({'error': 'Invalid form data.'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)
    


def store_data(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        requester_name = data.get('requester_name', '')

        # Save the data to the database
        RequestData.objects.create(requester_name=requester_name)
        
        return JsonResponse({'message': 'Data stored successfully'})
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
def get_data(request):
    if request.method == 'GET':
        # Retrieve all stored data from the database
        data = list(RequestData.objects.values())
        return JsonResponse(data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'})