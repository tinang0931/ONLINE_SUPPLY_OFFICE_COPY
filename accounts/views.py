from django.shortcuts import redirect, render
from .models import *
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
import random

def main(request):
    return render(request, 'accounts/User/main.html')


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
           return redirect('notification')
        else:
            # Authentication failed, show an error message
            messages.error(request, "Invalid login credentials. Please try again.")
    return render(request, 'accounts/User/login.html')


@unauthenticated_user  
def handle_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        print('sfsdfsdgfdfgf')

        # Check if the email exists in the database (you need to implement this)
      
            # Generate a random 4-digit verification code
        verification_code = get_random_string(4, '0123456789')
        print('sfsdfsdgfdfgf')

            # Save the verification code and link it to the user's email in the database
        VerificationCode.objects.create(email=email, code=verification_code)
        print('sfsdfsdgfdfgf')

            # Send the verification code to the user's email
        subject = 'Password Reset Verification Code'
        message = f'Your verification code is: {verification_code}'
        from_email = 'rlphtzn@gmail.com'  # Replace with your email address
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)
        print('sfsdfsdgfdfgf')

            # Redirect the user to a page where they can enter the verification code
        return redirect('verify_code')  # You need to create a 'verify_code' URL pattern
    return render(request, 'accounts/User/forgot.html')


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


@unauthenticated_user
# This view should handle the verification and password reset
def verify_code(request):
    if request.method == 'POST':
        code1 = request.POST.get('code1')
        code2 = request.POST.get('code2')
        code3 = request.POST.get('code3')
        code4 = request.POST.get('code4')

        # Combine the 4 input fields into a single code
        verification_code = f"{code1}{code2}{code3}{code4}"

        # Perform code verification here (compare with the one sent to the user's email)

        # If the code is valid, you can redirect to a password reset form
        if is_valid_code(verification_code):
            return redirect('reset_password')  # Create this URL pattern
    return render(request, 'accounts/User/verify.html')  # Adjust the template name


# This function should be implemented to verify the code
def is_valid_code(verification_code):
    # You need to implement your code verification logic here
    # Verify the code against the code you sent via email
    # Return True if the code is valid, or False otherwise

# You'll also need to create a view and URL pattern for resetting the password
    pass



def logout_user(request):
    logout(request)
    messages.success(request, ("You are now successfully logout."))
    return redirect('homepage')



def about(request):
    return render(request, 'accounts/User/about.html')



def history(request):
    return render(request, 'accounts/User/history.html')



def tracker(request):
    return render(request, 'accounts/User/tracker.html')



def notification(request):
    return render(request, 'accounts/User/notification.html')



def pro_file(request):
    return render(request, 'accounts/User/pro_file.html')



def profile(request):
    return render(request, 'accounts/User/profile.html')



def profile_html(request):
    return render(request, 'profile.html')



def notification_html(request):
    return render(request, 'notification.html')


def pro_file_html(request):
    return render(request, 'pro_file.html')



def about_cash(request):
    return render(request, 'accounts/Admin/Accounting/about_cash.html')


def cash_disbursement(request):
    return render(request, 'accounts/Admin/Accounting/cash_disbursement.html')



def home_cash(request):
    return render(request, 'accounts/Admin/Accounting/home_cash.html')



def prequest(request): # type: ignore
    return render(request, 'accounts/Admin/Accounting/prequest.html')



def reward_cash(request):
    return render(request, 'accounts/Admin/Accounting/reward_cash.html')



def form(request):
    return render(request, 'accounts/Admin/Accounting/form.html')



def prequest(request):
    return render(request, 'accounts/Admin/Accounting/prequest.html')



def campus_director_requester(request):
    return render(request, 'accounts/Admin/campusD/requester.html')



def campus_director_notification(request):
    return render(request, 'accounts/Admin/campusD/notification.html')



def campus_director_resolution(request):
    return render(request, 'accounts/Admin/campusD/resolution.html')



def campus_director_historycd(request):
    return render(request, 'accounts/Admin/campusD/historycd.html')



def campus_director_about(request):
    return render(request, 'accounts/Admin/campusD/about.html')



def supply_office_home(request):
    return render(request, 'accounts/Admin/Supply_office/home.html')



def home(request):
    return render(request, 'accounts/Accounting/home.html')


@authenticated_user
def signout(request):

    pass

def about_cash(request):
    return render(request, 'accounts/Admin/Accounting/about_cash.html')

def cash_disbursement(request):
    return render(request, 'accounts/Admin/Accounting/cash_disbursement.html')

def home_cash(request):
    return render(request, 'accounts/Admin/Accounting/home_cash.html')

def prequest(request):
    return render(request, 'accounts/Admin/Accounting/prequest.html')

def form(request):
    return render(request, 'accounts/Admin/Accounting/form.html')

def decline(request):
    return render(request, 'accounts/Admin/Accounting/decline.html')

def notice_of_reward(request):
    return render(request, 'accounts/Admin/Accounting/notice_of_reward.html')

def prequest(request):
    return render(request, 'accounts/Admin/Accounting/prequest.html')


def campus_director_requester(request):
    return render(request, 'accounts/Admin/campusD/requester.html')

def campus_director_notification(request):
    return render(request, 'accounts/Admin/campusD/notification.html')

def campus_director_resolution(request):
    return render(request, 'accounts/Admin/campusD/resolution.html')

def campus_director_historycd(request):
    return render(request, 'accounts/Admin/campusD/historycd.html')

def campus_director_about(request):
    return render(request, 'accounts/Admin/campusD/about.html')

def supply_office_home(request):
    return render(request, 'accounts/Admin/Supply_office/home.html')


def home(request):
    return render(request, 'accounts/Accounting/home.html')


def signout(request):
    pass

def supply_office_notification(request):
    return render(request, 'accounts/Admin/Supply_office/notification.html')


def supply_office_history(request):
    return render(request, 'accounts/Admin/Supply_office/history.html')


def supply_office_about(request):
    return render(request, 'accounts/Admin/Supply_office/about.html')


def supply_office_inventory(request):
    return render(request, 'accounts/Admin/Supply_office/inventory.html')


def notice_of_reward(request):
    return render(request, 'accounts/Admin/Accounting/notice_of_reward.html')


def about_bac(request):
    return render(request, 'accounts/Admin/BAC/about_bac.html')


def home_bac(request):
    return render(request, 'accounts/Admin/BAC/home_bac.html')


def purchase_bac(request):
    return render(request, 'accounts/Admin/BAC/purchase_bac.html')


def sahomepage(request):
    return render(request, 'accounts/Admin/BAC/sahomepage.html')


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
    if request.method == "POST":
        name = request.POST.get('item_name[]', '')
        description = request.POST.get('item_description[]', '')
        quantity = int(request.POST.get('quantity[]', 0))
        unit = request.POST.get('unit[]', '')
        unit_cost = float(request.POST.get('unit_cost[]', 0))
        purpose = request.POST.get('item_purpose', '')
        department_option = request.POST.get('departmentDropdown', '')  # Get the selected department option

        # Map the selected option to the department name
        department_name = department_mapping.get(department_option, '')

        # Get the user's ID from the logged-in user
        user_id = request.user.id

        # Create and save the item with the user_id
        item = Item(
            name=name,
            description=description,
            quantity=quantity,
            unit=unit,
            unit_cost=unit_cost,
            department=department_name,
            purpose=purpose,
            user_id=user_id  # Include the user_id in the item
        )
        item.save()

        messages.success(request, "Item added successfully.")
        return redirect('requester')  # Redirect to the same page after submissio
    return render(request, 'accounts/User/requester.html')



def transaction_history(request):
    # Retrieve and display the transaction history
    transaction_history = TransactionHistory.objects.filter(user=request.user).order_by('-date')
    return render(request, 'accounts/User/History.html', {'transaction_history': transaction_history})




