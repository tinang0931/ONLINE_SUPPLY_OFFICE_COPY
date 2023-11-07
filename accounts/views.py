from django.shortcuts import redirect, render
from .models import *
from django.contrib import messages
from django.shortcuts import render
from .models import Item
from .models import Department, Item, Purpose
from django.http import JsonResponse
from django.contrib.auth import authenticate, login as auth_login, logout
from .decorators import unauthenticated_user, authenticated_user
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from .tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth import update_session_auth_hash
from django.utils.crypto import get_random_string
from django.core.cache import cache
from django.core.mail import send_mail
import random
from django.shortcuts import render, redirect, get_object_or_404
from .models import PurchaseRequest



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
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')  # Use 'pass1' as the password field name
        
        # Authenticate the user
        user = authenticate(request, username=username, password=pass1)
        if user is not None and user.is_active:
    # User is valid and active, log them in
           auth_login(request, user)
           messages.success(request, "You are now logged in.")
           return redirect('requester')
        else:
            # Authentication failed, display an error message
            messages.error(request, 'Invalid login credentials. Please try again.')
    
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



@authenticated_user
def logout_user(request):
    logout(request)
    messages.success(request, ("You are now successfully logout."))
    return redirect('homepage')


@authenticated_user
def about(request):
    return render(request, 'accounts/User/about.html')


@authenticated_user
def item_selection(request):
    return render(request, 'accounts/User/item_selection.html')


@authenticated_user
def history(request):
   user_history = History.objects.filter(user=request.user).order_by('-date_requested')
   return render(request, 'accounts/User/history.html')


@authenticated_user
def tracker(request):
    return render(request, 'accounts/User/tracker.html')


@authenticated_user
def pro_file(request):
    return render(request, 'accounts/User/pro_file.html')


@authenticated_user
def prof(request):
    return render(request, 'accounts/User/prof.html')


@authenticated_user
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
def profile_html(request):
    return render(request, 'profile.html')


@authenticated_user
def pro_file_html(request):
    return render(request, 'pro_file.html')


@authenticated_user
def signout(request):
    pass


department_mapping = {
    'option1': 'College of Arts and Sciences',
    'option2': 'College of Agriculture',
    'option3': 'College of Forestry',
    'option4': 'College of Hospitality Management and Tourism',
    'option5': 'College of Technology and Engineering',
    'option6': 'College of Education',
    'option7': 'Graduate School',
}


@authenticated_user
def requester(request):
    if request.method == 'POST':
        print("dfsdffsdfs")
        # Handle department selection
        department_id = request.POST.get('departmentDropdown')
        if department_id == 'option8':
            # If "Others" department is selected, use the custom department input
            department_name = request.POST.get('customDepartment')
        else:
            # Use the selected department from the dropdown
            department = Department.objects.get(pk=department_id)
            department_name = department.name
        print("dfsdffsdfs")

        # Create an Item object and populate its fields with form data
        item = Item(
            department=department_name,
            item_number=request.POST.get('item_number'),
            item_name=request.POST.get('item_name'),
            item_description=request.POST.get('item_description'),
            unit=request.POST.get('unit'),
            unit_cost=request.POST.get('unit_cost'),
            quantity=request.POST.get('quantity'),
            total_cost=request.POST.get('total_cost')
        
        )
        print("dfsdffsdfs")
        item.save() 
        print("dfsdffsdfs") # Save the Item object to the database

        # Handle the purpose field if needed
        purpose_text = request.POST.get('item_purpose')
        if purpose_text:
            purpose = Purpose(item=item, description=purpose_text)
            purpose.save()
        print("dfsdffsdfs")
        # You can return a success message or redirect to another page
        return JsonResponse({'message': 'Data saved to the database'})

    # Handle GET requests or other cases as needed
    # ...

    return render(request, 'accounts/User/requester.html' )




def tracker(request):
    def __init__(request, product_id, department, purpose, item, date_requested, ctu_id, campus_director_approval, bac_secretariat_resolution, budget_officer_approval, date_status_update, status):
        request.product_id = product_id
        request.department = department
        request.purpose = purpose
        request.item = item
        request.date_requested = date_requested
        request.ctu_id = ctu_id
        request.campus_director_approval = campus_director_approval
        request.bac_secretariat_resolution = bac_secretariat_resolution
        request.budget_officer_approval = budget_officer_approval
        request.date_status_update = date_status_update
        request.status = status
        
    def get_product_id(request):
        return request.product_id
    
    def set_product_id(request, product_id):
        request.product_id = product_id
        
    def get_status(request):
        return request.status
    
    def set_status(self, status):
        self.status = status
        
    tracker = tracker.objects.all()
    context = {
            'product_id' : request.product_id,
            'department' : request.department,
            'purpose' : request.purpose,
            'item' : request.item,
            'date_requested': request.date_requested.strftime('%Y-%m-%d'),  # Format date as a string
            'ctu_id': request.ctu_id,
            'campus_director_approval': request.campus_director_approval,
            'bac_secretariat_resolution': request.bac_secretariat_resolution,
            'budget_officer_approval': request.budget_officer_approval,
            'date_status_update': request.date_status_update.strftime('%Y-%m-%d'),  # Format date as a string
            'status': request.status,
        }
    return render(request, 'accounts/User/tracker.html')

