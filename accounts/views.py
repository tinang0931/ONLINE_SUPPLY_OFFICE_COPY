from audioop import reverse
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
from .decorators import unauthenticated_user, authenticated_user, admin_required, regular_user_required
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
from .models import User
from .forms import UserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import random
import pandas as pd
from itertools import groupby
from django.core.files.base import ContentFile



def main(request):
    return render(request, 'accounts/User/main.html')


def Procurement(request):
    class proc:
        def __init__(self, category, item,unit,budget,jan,feb,march,april,may,june,july,aug,sep,oct,nov,dec,price) -> None:
            self.category = category
            self.item = item,
            self.unit = unit,
            self.budget = budget,
            self.jan = jan,
            self.feb = feb,
            self.march = march,
            self.april = april,
            self.may = may,
            self.june = june,
            self.july = july,
            self.aug = aug,
            self.sep = sep,
            self.oct = oct,
            self.nov = nov,
            self.dec = dec,
            self.price = price
    
    procure = []
    df = pd.read_csv('categories.csv')
    categories = df['categories']
    for c in categories:
        cat = pd.read_csv(f'categories\{c}.csv')
        for index, row in cat.iterrows():
            p = proc(c, row['item'], row['unit'],row['budget'],row['jan'],row['feb'],row['march'],row['april'],row['may'],row['june'],row['july'],row['aug'],row['sep'],row['oct'],row['nov'],row['dec'],row['price'])
            procure.append(p)
    
    
    grouped_data = {}
    for item in procure:
        category = item.category
        if category not in grouped_data:
            grouped_data[category] = []
        grouped_data[category].append(item)
    context = {
        'grouped_data':grouped_data
    }
    return render(request, 'accounts/User/Procurement.html', context)


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

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'accounts/User/register.html')
        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email is already in use.")
            return render(request, 'accounts/User/register.html')

        user = User.objects.create_user(username=username, email=email, password=password1, contact1=contact1, contact2=contact2,  user_type=user_type, is_active=False)
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
        messages.success(request, "Your account has been successfully created. Check your email for activation instructions.")
        return redirect('login')
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
        pass1 = request.POST.get('pass1')
          
        user = authenticate(request, username=username, password=pass1)
        if user is not None and user.is_active:
            auth_login(request, user)
            messages.success(request, "You are now logged in.")

            # Redirect based on user_type
            if user.user_type == 'admin':
                return redirect('admin_home')  
            elif user.user_type == 'regular':
                return redirect('request')
            elif user.user_type == 'cd':
                return redirect('cd')
            elif user.user_type == 'budget':
                return redirect('bo')
            elif user.user_type == 'bac':
                return redirect('bac_home')
            else:
                return redirect('login') 
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
    
    return render(request, 'accounts/User/login.html') 
def bac_home(request):
    if not request.user.is_admin:
        return redirect('request')

def request_page(request):
    if request.user.is_admin:
        return redirect('bac_home')
    return render(request, 'request.html')


def get_random_string(length, allowed_chars='0123456789'):
    return ''.join(random.choice(allowed_chars) for _ in range(length))


def handle_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        verification_code = get_random_string(4, '0123456789')
        cache_key = f'verification_code_{email}'
        cache.set(cache_key, verification_code, 600) 
        subject = 'Password Reset Verification Code'
        message = f'Your verification code is: {verification_code}'
        from_email = 'rlphtzn@gmail.com'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)
        return redirect('verify_code')  
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
            return redirect('reset_password')  
    return render(request, 'accounts/User/verify.html')  


def is_valid_code(verification_code, user_email):
    cache_key = f'verification_code_{user_email}'
    stored_code = cache.get(cache_key)
    if stored_code and verification_code == stored_code:
        return True
    return False


def reset_password(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')  
        user = request.user  
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        messages.success(request, 'Password updated successfully.')
        return redirect('login') 
    return render(request, 'accounts/User/reset.html') 


@authenticated_user
def logout_user(request):
    logout(request)
    messages.success(request, "You are now logged out.")
    return redirect('login')


@authenticated_user
def about(request):
    return render(request, 'accounts/User/about.html')

@authenticated_user
def registration(request):
    return render(request, 'accounts/User/registration.html')

@regular_user_required
def regular_user_only_view(request):
    return render(request, 'accounts/User/request.html')


@authenticated_user
def history(request):
    user = request.user
    all_checkouts = Checkout.objects.filter(user=user)
    all_checkout_items = CheckoutItems.objects.filter(checkout__in=all_checkouts)
    context = {
        'checkout_items': all_checkout_items,
    }
    return render(request, 'accounts/User/history.html', context)


@authenticated_user
def tracker(request):
    user = request.user
    all_checkouts = Checkout.objects.filter(user=user)
    feedback = Comment.objects.filter(pr_id__in=[checkout.pr_id for checkout in all_checkouts])
    context = {'feedback': feedback, 'checkout_info': all_checkouts}
    return render(request, 'accounts/User/tracker.html', context)

@authenticated_user
@regular_user_required
def prof(request):
    return render(request, 'accounts/User/prof.html')


@authenticated_user
@regular_user_required
def profile(request):
    return render(request, 'accounts/User/profile.html')

@authenticated_user
def bac_about(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_about.html')


@authenticated_user
def bac_home(request):
    checkouts = Checkout.objects.select_related('user').all()
    comments = Comment.objects.all()
    checkout_data_dict = {}

    for checkout in checkouts:
        pr_id = checkout.pr_id
        latest_comment = comments.filter(pr_id=pr_id).order_by('-timestamp').first()

        if pr_id not in checkout_data_dict:
            checkout_data_dict[pr_id] = {
                'pr_id': pr_id,
                'first_name': checkout.user.first_name,
                'last_name': checkout.user.last_name,
                'submission_date': checkout.submission_date,
                'purpose': checkout.purpose,
                'status_comment': latest_comment.content if latest_comment else "",
                'status_update_date': latest_comment.timestamp if latest_comment else None,
                'is_approve':checkout.is_approve
            }
        else:
            checkout_data_dict[pr_id]['purpose'] += f", {checkout.purpose}"
   
            # Update the status-related fields
            checkout_data_dict[pr_id]['is_approve'] = checkout.is_approve
            checkout_data_dict[pr_id]['is_disapprove'] = checkout.is_disapprove
            checkout_data_dict[pr_id]['is_seen'] = checkout.is_seen
            checkout_data_dict[pr_id]['status_comment'] = latest_comment.content if latest_comment else ""
            checkout_data_dict[pr_id]['status_update_date'] = latest_comment.timestamp if latest_comment else None

   
    checkout_data = list(checkout_data_dict.values())
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_home.html', {'checkouts': checkout_data})
from django.urls import reverse
class PreqFormView(View):
    template_name = 'accounts/Admin/BAC_Secretariat/preqform.html'
    def get(self, request, pr_id):
        checkout = Checkout.objects.get(pr_id=pr_id)
        checkout_items = CheckoutItems.objects.filter(checkout=checkout)
        context = {
            'checkout_items': checkout_items,
            'pr_id': pr_id,
            'user': checkout.user,
            'purpose': checkout.purpose,
        }
        return render(request, self.template_name, context)

    def post(self, request, pr_id):
        content = request.POST.get('comment_content')
        if pr_id and content:
            try:
                Comment.objects.create(content=content, timestamp=timezone.now(), pr_id=pr_id)
                return redirect(reverse('preqform', kwargs={'pr_id': pr_id}))
            except Exception as e:
                print(f"Error: {e}")
                return HttpResponse("An error occurred while processing the form.")
        else:
            return HttpResponse("PR ID or comment content not found in the form data.")
        

@authenticated_user
def np(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/np.html')


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
def purchaseorder(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/purchaseorder.html')


@authenticated_user
def inspection(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/inspection.html')


@authenticated_user
def property(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/property.html')


@authenticated_user
def np(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/np.html')


@authenticated_user
def notif(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/notif.html')


@authenticated_user
def abstract(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/abstract.html')
@authenticated_user
def bac_prof(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_prof.html')
@authenticated_user
def bac_profile(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_profile.html')

@authenticated_user
def bo(request):
    return render(request, 'accounts/Admin/Budget_Officer/bo.html')


@authenticated_user
def boabout(request):
    return render(request, 'accounts/Admin/Budget_Officer/boabout.html')


@authenticated_user
def bohistory(request):
    return render(request, 'accounts/Admin/Budget_Officer/bohistory.html')


@authenticated_user
def cd(request):
    return render(request, 'accounts/Admin/Campus_Director/cd.html')


@authenticated_user
def cdabout(request):
    return render(request, 'accounts/Admin/Campus_Director/cdabout.html')


@authenticated_user
def cdpurchase(request):
    return render(request, 'accounts/Admin/Campus_Director/cdpurchase.html')


@authenticated_user
def cdresolution(request):
    return render(request, 'accounts/Admin/Campus_Director/cdresolution.html')


@authenticated_user
def resolution(request):
    return render(request, 'accounts/Admin/Campus_Director/resolution.html')



@authenticated_user
def profile_html(request):
    return render(request, 'profile.html')

@authenticated_user
def purchaseorder(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/purchaseorder.html')

@authenticated_user
def admin_home(request):
    return render(request, 'accounts/Admin/System_Admin/admin_home.html')



@authenticated_user
def adminabout(request):
    return render(request, 'accounts/Admin/System_Admin/adminabout.html')


@authenticated_user
def user(request):
    users = User.objects.all()
    return render (request, 'accounts/Admin/System_Admin/user.html',{'users': users})



# def update_user(request, username):
#     user = get_object_or_404(User, username=username)

#     if request.method == 'POST':
#         form = UserForm(request.POST, instance=user)
#         if form.is_valid():
#             form.save()
#             return redirect('user')
#     else:
#         form = UserForm(instance=user) 
#         return render(request, 'accounts/Admin/System_Admin/user.html', {'form': form})

def register_user(request):
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

        if password1 != password2:
            messages.error(request, "Passwords do not match.")

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email is already in use.")
            

        user = User.objects.create_user(username=username, email=email, password=password1, contact1=contact1, contact2=contact2,  user_type=user_type, is_active=False)
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
        messages.success(request, "The account has been successfully created. Check the email for activation instructions.")
        return redirect('user')
    
   



def update_user(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'User updated successfully'})  # Return a success message
        else:
            return JsonResponse({'error': form.errors}, status=400)  # Return form errors if not valid
    else:
        form = UserForm(instance=user) 
        return render(request, 'edit_user.html', {'form': form, 'user': user})


   
def delete_user(request, username):
    user = User.objects.get(username=username)
    user.delete()
    return redirect('user')


def addItem(request):
    if request.method == 'POST':
        item_data = request.POST.get('item')
        item_brand_description = request.POST.get('item_Brand_Description')
        unit = request.POST.get('unit')
        unit_cost = request.POST.get('unit_Cost')
        quantity = request.POST.get('quantity')

        if quantity and quantity.isdigit():
                quantity = int(quantity)
        else:

            print("Invalid quantity")
            return redirect('request')
        
        user = request.user
        Item.objects.create(
            user=user,
            item=item_data,
            item_brand_description=item_brand_description,
            unit=unit,
            unit_cost=unit_cost,
            quantity=quantity,
             total_cost=float(unit_cost) * quantity,
            
        )
        return redirect('request')
    return render(request, 'accounts/User/request.html')


def request(request):
    if request.method == 'POST':

        selected_rows = request.POST.getlist('selectRow')

        for row_id in selected_rows:
            item_name = request.POST.get(f'item_{row_id}')
            item_brand = request.POST.get(f'item_brand_{row_id}')
            unit = request.POST.get(f'unit_{row_id}')
            price = request.POST.get(f'price_{row_id}')
            quantity = request.POST.get(f'quantity_{row_id}')

        
            if quantity and quantity.isdigit():
                quantity = int(quantity)
            else:
               
                print(f"Invalid quantity for row {row_id}")
                continue

            user = request.user


            item = Item.objects.create(
                user=user,
                item=item_name,
                item_brand_description=item_brand,
                unit=unit,
                unit_cost=price,
                quantity=quantity,

                total_cost=float(price) * quantity,
            )
            item.save()

        return redirect('requester')

    elif request.method == 'GET':
        csv_data = CSV.objects.all()
        grouped_data = {}
        for key, group in itertools.groupby(csv_data, key=lambda x: x.Category):
            grouped_data[key] = list(group)
    return render(request, 'accounts/User/request.html', {'grouped_data': grouped_data})


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_file_extension(value):
    valid_extensions = ['.pdf', '.doc', '.docx', '.jpg', '.png', '.xls', '.xlsx']
    extension = value.lower().split('.')[-1]

    if extension not in valid_extensions:
        raise ValidationError(_("File type is not supported. Supported types: .pdf, .doc, .docx, .jpg, .png, .xls, .xlsx"))

def validate_file_size(value):
    max_size = 5 * 1024 * 1024  # 5 MB

    if value.size > max_size:
        raise ValidationError(_("File size exceeds the maximum allowed size (5 MB)"))

class RequesterView(View):
    template_name = 'accounts/User/cart.html'

    def get(self, request):
        items = Item.objects.all()
        return render(request, self.template_name, {'items': items})

    def post(self, request):
        if request.method == 'POST':
            # Fetch data from the Item model
            items = Item.objects.all()
            purpose = request.POST.get('purpose', '') 
            new_checkout = Checkout.objects.create(user=request.user, pr_id=self.generate_pr_id(), purpose=purpose)

            for row in items:
                item_id = row.id
                item = request.POST.get(f'item_{item_id}')
                item_brand = request.POST.get(f'item_brand_{item_id}')
                unit = request.POST.get(f'unit_{item_id}')
                quantity = int(request.POST.get(f'quantity_{item_id}', 0)) 
                price = Decimal(request.POST.get(f'price_{item_id}', '0.00')) 
                

                try:
                    total_cost = price * quantity
                except TypeError:
                    total_cost = Decimal('0.00')


                CheckoutItems.objects.create(
                    checkout=new_checkout,
                    item=item,
                    item_brand_description=item_brand,
                    unit=unit,
                    quantity=quantity,
                    unit_cost=price,
                    total_cost=total_cost,
                )

            new_checkout.save()
            items.delete()
            return redirect('history')
    def generate_pr_id(self):
        random_number = str(random.randint(10000000, 99999999))
        return f"{random_number}_{timezone.now().strftime('%Y%m%d%H%M%S')}"


@authenticated_user
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})


@authenticated_user
def bac_history(request):
   request = Item.objects.all()
   return render(request,  'accounts/Admin/BAC_Secretariat/bac_history.html', {'request': request})


class GetNewRequestsView(View):
    def get(self, request, *args, **kwargs):
        new_requests = Checkout.objects.exclude(pr_id=None)
        serialized_requests = [
            {
                'user_id': request.user_id,
                'submission_date': request.submission_date,
            }
            for request in new_requests
        ]
        return JsonResponse({'new_requests': serialized_requests})
    

             
def delete(request, id):
    item = Item.objects.get(id = id)
    item.delete()
    return redirect ('requester')

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





def bac_dashboard(request):
    if request.method == 'GET':
        csv_data = CSV.objects.all().order_by('Category')
        grouped_data = {}
        for key, group in itertools.groupby(csv_data, key=lambda x: x.Category):
            grouped_data[key] = list(group)
        
    

        return render(request, 'accounts/Admin/BAC_Secretariat/bac_dashboard.html', {'grouped_data': grouped_data})

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
    

def delete_category(request, Category):
    items_to_delete = CSV.objects.filter(Category=Category)
    items_to_delete.delete()



def bohome(request):
    checkouts = Checkout.objects.select_related('user').all()
    comments = Comment.objects.all()

    # Create a dictionary to store the results, using pr_id as keys
    checkout_data_dict = {}

    # Loop through each Checkout instance and gather relevant data
    for checkout in checkouts:
        pr_id = checkout.pr_id

        # Get the latest comment for the current pr_id
        latest_comment = comments.filter(pr_id=pr_id).order_by('-timestamp').first()

        if pr_id not in checkout_data_dict:
            # If pr_id is not in the dictionary, create a new entry
            checkout_data_dict[pr_id] = {
                'pr_id': pr_id,
                'first_name': checkout.user.first_name,
                'last_name': checkout.user.last_name,
                'submission_date': checkout.submission_date,
                'purpose': checkout.purpose,
                'is_approve': checkout.is_approve,
                'is_disapprove': checkout.is_disapprove,
                'is_seen': checkout.is_seen,  # Include the new field in the view
                'comment': latest_comment.content if latest_comment else "",
                'status_update_date': latest_comment.timestamp if latest_comment else None,
                 
            }
        else:
            # If pr_id is already in the dictionary, update the entry
            # with additional information, e.g., concatenate purposes
            checkout_data_dict[pr_id]['purpose'] += f", {checkout.purpose}"
           
            checkout_data_dict[pr_id]['status_update_date'] = latest_comment.timestamp if latest_comment else None
    # Convert the dictionary values to a list
    checkout_data = list(checkout_data_dict.values())

    return render(request, 'accounts/Admin/Budget_Officer/bohome.html', {'checkouts': checkout_data})

class PreqForm_boView(View):
    template_name = 'accounts/Admin/Budget_Officer/preqform_bo.html'

    def get(self, request, pr_id):
        # Use the pr_id to retrieve the corresponding Checkout object
        checkout = get_object_or_404(Checkout, pr_id=pr_id)

        # Get checkout items associated with the checkout
        checkout_items = CheckoutItems.objects.filter(checkout=checkout)

        context = {
            'checkout_items': checkout_items,
            'pr_id': pr_id,
            'user': checkout.user,
            'purpose': checkout.purpose,
            'pending': not checkout.is_approve and not checkout.is_disapprove,
            'approved': checkout.is_approve,
            'disapproved': checkout.is_disapprove,
            'is_seen': checkout.is_seen,
            
        }

        return render(request, self.template_name, context)

    def post(self, request, pr_id):
        new_status = request.POST.get('new_status')

        if pr_id and new_status:
            try:
                checkout = Checkout.objects.get(pr_id=pr_id)

                checkout.date_updated = timezone.now()
                checkout.is_seen = True

                # Set is_approve and is_disapprove to False initially
                checkout.is_approve = False
                checkout.is_disapprove = False

                if new_status.lower() == 'true':
                    checkout.is_approve = True
                else:
                    checkout.is_disapprove = True

                checkout.save()

                return redirect(reverse('preqform_bo', kwargs={'pr_id': pr_id}))
            except Checkout.DoesNotExist:
                return HttpResponse("Checkout not found.")
            except Exception as e:
                print(f"Error: {e}")
                return HttpResponse("An error occurred while processing the form.")
        else:
            return HttpResponse("PR ID or new status not found in the form data.")


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
def purchaseorder(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/purchaseorder.html')

@authenticated_user
def inspection(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/inspection.html')

@authenticated_user
def property(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/property.html')

@authenticated_user
def np(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/np.html')
@authenticated_user
def notif(request):
    return render(request, 'accounts/Admin/BAC_Secretariat/notif.html')
@authenticated_user
def abstract(request):
    # Your view logic here
    return render(request, 'accounts/Admin/BAC_Secretariat/abstract.html')


def addItem(request):
    if request.method == 'POST':
        item_data = request.POST.get('item')
        item_brand_description = request.POST.get('item_Brand_Description')
        unit = request.POST.get('unit')
        unit_cost = request.POST.get('unit_Cost')
        quantity = request.POST.get('quantity')

        if quantity and quantity.isdigit():
                quantity = int(quantity)
        else:

            print("Invalid quantity")
            return redirect('request')
        
        user = request.user
        Item.objects.create(
            user=user,
            item=item_data,
            item_brand_description=item_brand_description,
            unit=unit,
            unit_cost=unit_cost,
            quantity=quantity,
             total_cost=float(unit_cost) * quantity,
            
        )
        return redirect('request')
    return render(request, 'accounts/User/request.html')

def request(request):
    if request.method == 'POST':

        selected_rows = request.POST.getlist('selectRow')

        for row_id in selected_rows:
            item_name = request.POST.get(f'item_{row_id}')
            item_brand = request.POST.get(f'item_brand_{row_id}')
            unit = request.POST.get(f'unit_{row_id}')
            price = request.POST.get(f'price_{row_id}')
            quantity = request.POST.get(f'quantity_{row_id}')

        
            if quantity and quantity.isdigit():
                quantity = int(quantity)
            else:
               
                print(f"Invalid quantity for row {row_id}")
                continue

            user = request.user


            item = Item.objects.create(
                user=user,
                item=item_name,
                item_brand_description=item_brand,
                unit=unit,
                unit_cost=price,
                quantity=quantity,

                total_cost=float(price) * quantity,
            )
            item.save()

        return redirect('requester')

    elif request.method == 'GET':
        csv_data = CSV.objects.all()
        grouped_data = {}
        for key, group in itertools.groupby(csv_data, key=lambda x: x.Category):
            grouped_data[key] = list(group)
    return render(request, 'accounts/User/request.html', {'grouped_data': grouped_data})

def cdpurchase(request):
    checkouts = Checkout.objects.select_related('user').all()
    comments = Comment.objects.all()

    checkout_data_dict = {}

    for checkout in checkouts:
        pr_id = checkout.pr_id

        latest_comment = comments.filter(pr_id=pr_id).order_by('-timestamp').first()

        if pr_id not in checkout_data_dict:
            checkout_data_dict[pr_id] = {
                'pr_id': pr_id,
                'first_name': checkout.user.first_name,
                'last_name': checkout.user.last_name,
                'submission_date': checkout.submission_date,
                'purpose': checkout.purpose,
                'is_approve': checkout.is_approve,
                'is_disapprove': checkout.is_disapprove,
                'is_seen': checkout.is_seen,  
                'comment': latest_comment.content if latest_comment else "",
                'status_update_date': latest_comment.timestamp if latest_comment else None,
                 
            }
        else:
            checkout_data_dict[pr_id]['purpose'] += f", {checkout.purpose}"
           
            checkout_data_dict[pr_id]['status_update_date'] = latest_comment.timestamp if latest_comment else None
    checkout_data = list(checkout_data_dict.values())

    return render(request, 'accounts/Admin/Campus_Director/cdpurchase.html', {'checkouts': checkout_data})

class PreqForm_cdView(View):
    template_name = 'accounts/Admin/Campus_Director/preqform_cd.html'

    def get(self, request, pr_id):
        # Use the pr_id to retrieve the corresponding Checkout object
        checkout = get_object_or_404(Checkout, pr_id=pr_id)

        # Get checkout items associated with the checkout
        checkout_items = CheckoutItems.objects.filter(checkout=checkout)

        context = {
            'checkout_items': checkout_items,
            'pr_id': pr_id,
            'user': checkout.user,
            'purpose': checkout.purpose,
            'pending': not checkout.is_approve and not checkout.is_disapprove,
            'approved': checkout.is_approve,
            'disapproved': checkout.is_disapprove,
            'is_seen': checkout.is_seen,
            
        }

        return render(request, self.template_name, context)

    def post(self, request, pr_id):
        new_status = request.POST.get('new_status')

        if pr_id and new_status:
            try:
                checkout = Checkout.objects.get(pr_id=pr_id)

                checkout.date_updated = timezone.now()
                checkout.is_seen = True

                # Set is_approve and is_disapprove to False initially
                checkout.is_approve = False
                checkout.is_disapprove = False

                if new_status.lower() == 'true':
                    checkout.is_approve = True
                else:
                    checkout.is_disapprove = True

                checkout.save()

                return redirect(reverse('preqform_cd', kwargs={'pr_id': pr_id}))
            except Checkout.DoesNotExist:
                return HttpResponse("Checkout not found.")
            except Exception as e:
                print(f"Error: {e}")
                return HttpResponse("An error occurred while processing the form.")
        else:
            return HttpResponse("PR ID or new status not found in the form data.")

def update_checkout_status(request, pr_id, new_status):
    if request.method == 'POST':
        try:
            # Convert new_status to boolean
            new_status = new_status.lower() == 'true' if isinstance(new_status, str) else new_status

            # Update the status of the checkout directly
            checkout = get_object_or_404(Checkout, pr_id=pr_id)
            checkout.status_update_date = timezone.now()
            checkout.is_approve = new_status
            checkout.is_disapprove = not new_status
            checkout.is_seen = True  # Mark as seen when the status is updated
            checkout.save()

            # Redirect after processing
            return redirect(reverse('preqform_bo', kwargs={'pr_id': pr_id}))
        except Checkout.DoesNotExist:
            return HttpResponse("Checkout not found.")
        except Exception as e:
            # Handle exceptions, log errors, etc.
            print(f"Error: {e}")
            return HttpResponse("An error occurred while processing the form.")
    else:
        return HttpResponse("Invalid request method.")
    
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

@admin_required
@authenticated_user
def bac_history(request):
   request = Item.objects.all()

   return render(request,  'accounts/Admin/BAC_Secretariat/bac_history.html', {'request': request})


class GetNewRequestsView(View):
    def get(self, request, *args, **kwargs):

       

          # Fetch new requests from the database based on your criteria
        new_requests = Checkout.objects.exclude(pr_id=None)

        # Serialize the data as needed
        serialized_requests = [
            {
                'user_id': request.user_id,
                'submission_date': request.submission_date,
                # Add other fields as needed
            }
            for request in new_requests
        ]

        return JsonResponse({'new_requests': serialized_requests})

@authenticated_user              
def delete_item(request, id):
    item = Item.objects.get(id = id)
    item.delete()
    return redirect ('requester')
