from audioop import reverse
import json
from urllib.parse import parse_qs
from django.views import View
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

User = get_user_model()
@unauthenticated_user

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        contact1 = request.POST['contact1']
        contact2 = request.POST['contact2']
        password1 = request.POST['pass1']
        password2 = request.POST['pass2']
        user_type = request.POST['user_type']


        # Check if passwords match
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/User/register.html')

        # Check if the username or email is already in use
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email is already in use.")
            return render(request, 'accounts/User/register.html')

        # Create a new user account
        user = User.objects.create_user(username=username, email=email, password=password1, contact1=contact1, contact2=contact2,  user_type=user_type, is_active=False)
        user.first_name = first_name
        user.last_name = last_name
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
def registration(request):
    return render(request, 'accounts/User/registration.html')


def history(request):
    requests = CheckoutItems.objects.all()
    return render(request, 'accounts/User/history.html', {'requests': requests})

def tracker(request):
    status = Comment.objects.all()
    return render(request, 'accounts/User/tracker.html', {'status': status})
   

def prof(request):
    return render(request, 'accounts/User/prof.html')

def profile(request):
    return render(request, 'accounts/User/profile.html')

def bac_about(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_about.html')

def bac_history(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_history.html')

def bac_home(request):
   
    
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_home.html',)
def preqform(request):
    checkout_items = CheckoutItems.objects.all()

    if request.method == 'POST':
        content = request.POST.get('comment_content')

        if content:
            Comment.objects.create(content=content, timestamp=timezone.now())
            return redirect('preqform')
        else:
            return HttpResponse("Comment content cannot be empty.")

    context = {
        'checkout_items': checkout_items,
    }

    return render(request, 'accounts/Admin/BAC_Secretariat/preqform.html', context)
def np(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/np.html')

def purchaseorder(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/purchaseorder.html')

def bids(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bids.html')

def noa(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/noa.html')



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

        return redirect('request')

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
        csv_file_path = 'C:/Users/cardosa.kristineanne/Desktop/INVENTORY/ONLINE_SUPPLY_OFFICE_COPY/items.csv'

        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            csv_data = list(reader)
        
        # Pass data to the template
        return render(request, 'accounts/User/request.html', {'csv_data': csv_data})


class RequesterView(View):
    template_name = 'accounts/User/cart.html'

    def get(self, request):
         # Fetch data from the Item model and pass it to the template
        items = Item.objects.all()

        # Calculate total cost based on the items
        # ...

        return render(request, self.template_name, {'items': items})

    def post(self, request):
        if 'submit_button' in request.POST:
            # Fetch data from the Item model
            items = Item.objects.all()

            # Handle form submission
            purpose = request.POST.get('purpose', '')  # Retrieve the 'Purpose' value

            new_checkout = Checkout.objects.create()

            for row in items:
                item_id = row.id
                item = request.POST.get(f'item_{item_id}')
                item_brand = request.POST.get(f'item_brand_{item_id}')
                unit = request.POST.get(f'unit_{item_id}')
                quantity = request.POST.get(f'quantity_{item_id}')
                price = request.POST.get(f'price_{item_id}')

                # Customize the fields according to your CheckoutItems model
                CheckoutItems.objects.create(
                    checkout=new_checkout,
                    purpose=purpose,
                    item=item,
                    item_brand_description=item_brand,
                    unit=unit,
                    quantity=quantity,
                    unit_cost=price,
                    # Add other fields as needed
                )

                Item.objects.filter(id=item_id).delete()

            return redirect('requester')
        return render(request, self.template_name)

def delete_item(request, item_id):
    if request.method == 'POST':
        # Get the object to be deleted
        item = get_object_or_404(CheckoutItems, id=item_id)

        # Perform delete operation
        item.delete()

        # Return a JSON response indicating success
        return JsonResponse({'status': 'success'})
    else:
        # Return a JSON response indicating failure for non-POST requests
        return JsonResponse({'status': 'failure', 'message': 'Invalid request method'})


def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})



def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})



def show_more_details(request):
    if request.method == 'POST':
        request_id = request.POST.get('request_id', None)

        if request_id:
            # Fetch the relevant data based on request_id
            # You should replace this with your actual data retrieval logic

            # For demonstration purposes, let's assume you have a dictionary
            # with form_type and form_data
            form_type = request.POST.get('form_type', 'other')
            form_data = {
                'purchase_approval': {'field1': 'Value1', 'field2': 'Value2'},
                'resolution_approval': {'field3': 'Value3', 'field4': 'Value4'},
                'abstract_of_bids': {'field5': 'Value5', 'field6': 'Value6'},
                'notice_of_reward': {'field7': 'Value7', 'field8': 'Value8'},
                'notice_to_proceed': {'field9': 'Value9', 'field10': 'Value10'},
                'inspection_acceptance': {'field11': 'Value11', 'field12': 'Value12'},
                'property_acknowledgment': {'field13': 'Value13', 'field14': 'Value14'},
                'purchase_order': {'field15': 'Value15', 'field16': 'Value16'},
            }

            response_data = form_data.get(form_type, {})

            return JsonResponse(response_data)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)
def bac_history(request):
   requests = Item.objects.all()

   return render(request,  'accounts/Admin/BAC_Secretariat/bac_history.html', {'request': request})
def item_delete(request, request_id):
    item = get_object_or_404(Item, request_id=request_id)
    item.delete()
    # Redirect to an appropriate URL after deletion
    return redirect('requester')  # Replace 'requester' with your desired redirect URL name

