from audioop import reverse
from django.http import HttpResponseRedirect, JsonResponse
from typing import ItemsView
from django.shortcuts import redirect, render, get_object_or_404
from django.core.cache import cache
from .models import *
import pymongo
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .decorators import unauthenticated_user, authenticated_user
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.models import User
from django.http import HttpResponse  
from django.shortcuts import render, redirect   
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage 
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
from django.contrib import messages
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string
from .models import VerificationCode
from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from .forms import ItemForm

import random

def main(request):
    return render(request, 'accounts/User/main.html')


def bac(request):
    return render(request, 'accounts/User/bac.html')


def homepage(request):
    return render(request, 'accounts/User/homepage.html')


@unauthenticated_user
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


@unauthenticated_user
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


@unauthenticated_user
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


@unauthenticated_user
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


@unauthenticated_user
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


@authenticated_user
def prof(request):
    return render(request, 'accounts/User/prof.html')



def profile(request):
    return render(request, 'accounts/User/profile.html')


@authenticated_user
def bac_about(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_about.html')


@authenticated_user
def bac_history(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_history.html')


@authenticated_user
def bac_home(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_home.html')



@authenticated_user
def preqform(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/preqform.html')


@authenticated_user
def profile_html(request):
    return render(request, 'profile.html')


@authenticated_user
def signout(request):
    pass



@authenticated_user
def request(request):
    if request.method == 'POST':
        # Handle form submission
        purpose = request.POST.get('item_purpose')
        item_data = request.POST.get('item')
        item_brand_description = request.POST.get('item_Brand_Description')
        unit = request.POST.get('unit')
        unit_cost = request.POST.get('unit_Cost')
        quantity = request.POST.get('quantity')

        # Django model section
        # Create a new Item instance and set its attributes
        Item.objects.create(
            purpose=purpose,
            item=item_data,
            item_brand_description=item_brand_description,
            unit=unit,
            unit_cost=unit_cost,
            quantity=quantity,
            
        )

        return redirect('request')  # Redirect to the same page after adding the item

    else:
        # Handle data fetching for GET request
        # Connect to MongoDB
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['inventory']
        collection = db['Inventcol']

        # Fetch all documents from the 'inventcol' collection
        cursor = collection.find()

        # Prepare data by category
        categories = {}
        for document in cursor:
            category_name = document['CATEGORY']
            if category_name not in categories:
                categories[category_name] = []

            categories[category_name].append({
                "ITEM_BRAND": document.get('ITEM_BRAND', ''),
                "ITEMS": document['ITEMS'],
                "UNIT": document['UNIT'],
                "PRICE": document['PRICE']
            })

        # Render the HTML template with categorized data
        return render(request, 'accounts/User/request.html', {'categories': categories})




def requester(request):
    items = Item.objects.all()  # Fetch all Item instances from the database
    return render(request, 'accounts/User/cart.html', {'items': items})





# @authenticated_user
# def bac_history(request):
#     # Fetch all PurchaseRequest objects linked to the logged-in user
#     purchase_requests = PurchaseRequestForm.objects.filter(item__user=request.user)

#     if request.method == 'POST':
#         action = request.POST.get('Action')
#         purchase_request_id = request.POST.get('Purchase_Request_ID')

#         # Check if the 'Purchase_Request_ID' field is present
#         if not purchase_request_id:
#             return HttpResponse('Please fill in all the required fields.')

#         # Fetch the PurchaseRequest object from the database
#         try:
#             purchase_request = PurchaseRequestForm.objects.get(id=purchase_request_id)
#         except PurchaseRequestForm.DoesNotExist:
#             return HttpResponse('Purchase request not found.')

#         # Update the PurchaseRequest object based on the submitted action
#         if action == 'approve':
#             purchase_request.is_approved = True
#         elif action == 'disapprove':
#             purchase_request.is_disapproved = False
#         else:
#             return HttpResponse('Invalid action.')

#         # Save the updated PurchaseRequest object to the database
#         purchase_request.save()

#         # Redirect to the bac_history page
#         return render(request('bac_history'))
#     # Render the bac_history page with the list of PurchaseRequest objects
#     return render(request, 'bac_history.history', {'purchase_requests': purchase_requests})



def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors}, status=400)

    return render(request, 'cart.html', {'item': item})

def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        item.delete()
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'serror'}, status=400)


