from django.shortcuts import redirect, render
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from .decorators import unauthenticated_user, authenticated_user
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
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
from .tokens import account_activation_token

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
            'token': default_token_generator.make_token(user),
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
            print('fddzjkfds')

    return render(request, 'accounts/User/login.html')

@unauthenticated_user
def forgot(request):
    return render(request, 'accounts/User/forgot.html')


@unauthenticated_user
def reset(request):
    return render(request, 'accounts/User/reset.html')

@unauthenticated_user
def verify(request):
    return render(request, 'accounts/User/verify.html')

@authenticated_user
def logout_user(request):
    logout(request)
    messages.success(request, ("You are now successfully logout."))
    return redirect('homepage')

@authenticated_user
def about(request):
    return render(request, 'accounts/User/about.html')

@authenticated_user
def history(request):
    return render(request, 'accounts/User/history.html')


@authenticated_user
def notification(request):
    return render(request, 'accounts/User/notification.html')

@authenticated_user
def pro_file(request):
    return render(request, 'accounts/User/pro_file.html')
@authenticated_user
def profile(request):
    return render(request, 'accounts/User/profile.html')
@authenticated_user
def profile_html(request):
    return render(request, 'profile.html')
@authenticated_user
def notification_html(request):
    return render(request, 'notification.html')
@authenticated_user
def pro_file_html(request):
    return render(request, 'pro_file.html')
@authenticated_user
def about_cash(request):
    return render(request, 'accounts/Admin/Accounting/about_cash.html')
@authenticated_user
def cash_disbursement(request):
    return render(request, 'accounts/Admin/Accounting/cash_disbursement.html')
@authenticated_user
def home_cash(request):
    return render(request, 'accounts/Admin/Accounting/home_cash.html')
@authenticated_user
def prequest(request): # type: ignore
    return render(request, 'accounts/Admin/Accounting/prequest.html')
@authenticated_user
def reward_cash(request):
    return render(request, 'accounts/Admin/Accounting/reward_cash.html')
@authenticated_user
def form(request):
    return render(request, 'accounts/Admin/Accounting/form.html')
@authenticated_user
def prequest(request):
    return render(request, 'accounts/Admin/Accounting/prequest.html')
@authenticated_user
def campus_director_requester(request):
    return render(request, 'accounts/Admin/campusD/requester.html')
@authenticated_user
def campus_director_notification(request):
    return render(request, 'accounts/Admin/campusD/notification.html')
@authenticated_user
def campus_director_resolution(request):
    return render(request, 'accounts/Admin/campusD/resolution.html')
@authenticated_user
def campus_director_historycd(request):
    return render(request, 'accounts/Admin/campusD/historycd.html')
@authenticated_user
def campus_director_about(request):
    return render(request, 'accounts/Admin/campusD/about.html')
@authenticated_user
def supply_office_home(request):
    return render(request, 'accounts/Admin/Supply_office/home.html')
@authenticated_user
def home(request):
    return render(request, 'accounts/Accounting/home.html')
@authenticated_user
def signout(request):

    pass
@authenticated_user
def supply_office_notification(request):
    return render(request, 'accounts/Admin/Supply_office/notification.html')
@authenticated_user
def supply_office_history(request):
    return render(request, 'accounts/Admin/Supply_office/history.html')
@authenticated_user
def supply_office_about(request):
    return render(request, 'accounts/Admin/Supply_office/about.html')
@authenticated_user
def supply_office_inventory(request):
    return render(request, 'accounts/Admin/Supply_office/inventory.html')
@authenticated_user
def notice_of_reward(request):
    return render(request, 'accounts/Admin/Accounting/notice_of_reward.html')
@authenticated_user
def bac(request):
    return render(request, 'accounts/Admin/BAC/bac.html')
@authenticated_user
def home_bac(request):
    return render(request, 'accounts/Admin/BAC/home_bac.html')
@authenticated_user
def purchase_bac(request):
    return render(request, 'accounts/Admin/BAC/purchase_bac.html')


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

@authenticated_user
def sahomepage(request):
    return render(request, 'accounts/Admin/sahomepage.html')
