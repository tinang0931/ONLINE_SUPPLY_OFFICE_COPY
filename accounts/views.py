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
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt 
import random
import pandas as pd
from itertools import groupby
from django.core.files.base import ContentFile
from .models import CheckoutItems



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
                return redirect('myppmp')
            elif user.user_type == 'cd':
                return redirect('cdpurchase')
            elif user.user_type == 'budget':
                return redirect('bohome')
            elif user.user_type == 'bac':
                return redirect('bac_home')
            else:
                
                return redirect('login') 
        else:
            messages.error(request, "Invalid login credentials. Please try again.")
    
    return render(request, 'accounts/User/login.html') 



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
    checkouts = Checkout.objects.filter(user=user)

    
    return render(request, 'accounts/User/history.html', {'checkouts': checkouts})


@authenticated_user
def tracker(request):
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
        'user': request.user
        
        
    }
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
   
    return render(request, 'accounts/Admin/BAC_Secretariat/bac_home.html')
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
def borequest(request):
    return render(request, 'accounts/Admin/Budget_Officer/borequest.html')


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
def cdppmp(request):
    return render(request, 'accounts/Admin/Campus_Director/cdppmp.html')


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

    return render(request, 'accounts/User/request.html', {'grouped_data': grouped_data})

def myppmp (request):
    items = CheckoutItems.objects.all()

    return render(request, 'accounts/User/myppmp.html', {'items': items})


def ppmp(request):
    
    if request.method == 'POST':
        new_checkout = Checkout.objects.create(
            user=request.user,
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

        # Update the new_checkout object with the generated pr_id
        new_checkout.pr_id = pr_id
        new_checkout.save()
       

        return redirect('tracker')



    elif request.method == 'GET':
    
        items = Item.objects.all()
    
    return render(request, 'accounts/User/ppmp.html', {'items': items})

def purchase(request):
    return render(request, 'accounts/User/purchase.html')


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


                PR.objects.create(
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
    

@authenticated_user              
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
            
            'bo_comment': checkout.bo_comment,  # Replace with the actual attribute names
        }
        checkout_data.append(checkout_dict)

    context = {
        'checkouts': checkout_data,
        
    }

    return render(request, 'accounts/Admin/Budget_Officer/bohome.html', context)

    # checkouts = Checkout.objects.select_related('user').all()
    # comments = Comment.objects.all()

    # # Create a dictionary to store the results, using pr_id as keys
    # checkout_data_dict = {}

    # # Loop through each Checkout instance and gather relevant data
    # for checkout in checkouts:
    #     pr_id = checkout.pr_id

    #     # Get the latest comment for the current pr_id
    #     latest_comment = comments.filter(pr_id=pr_id).order_by('-timestamp').first()

    #     if pr_id not in checkout_data_dict:
    #         # If pr_id is not in the dictionary, create a new entry
    #         checkout_data_dict[pr_id] = {
    #             'pr_id': pr_id,
    #             'first_name': checkout.user.first_name,
    #             'last_name': checkout.user.last_name,
    #             'submission_date': checkout.submission_date,
    #             'purpose': checkout.purpose,
    #             'is_approve': checkout.is_approve,
               
    #             'is_seen': checkout.is_seen,  # Include the new field in the view
    #             'comment': latest_comment.content if latest_comment else "",
    #             'status_update_date': latest_comment.timestamp if latest_comment else None,
                 
    #         }
    #     else:
    #         # If pr_id is already in the dictionary, update the entry
    #         # with additional information, e.g., concatenate purposes
    #         checkout_data_dict[pr_id]['purpose'] += f", {checkout.purpose}"
           
    #         checkout_data_dict[pr_id]['status_update_date'] = latest_comment.timestamp if latest_comment else None
    # # Convert the dictionary values to a list
    # checkout_data = list(checkout_data_dict.values())

    # return render(request, 'accounts/Admin/Budget_Officer/bohome.html', {'checkouts': checkout_data})
def bo_approve(request, pr_id):
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
            bo_comment=comment_content
        )

        return redirect('bohome')

    elif request.method == 'GET':
        checkouts = get_object_or_404(Checkout, pr_id=pr_id)
        checkout_items = CheckoutItems.objects.filter(checkout=checkouts)
        context = {
            'checkouts': checkouts,
            'checkout_items': checkout_items,
            'pr_id': pr_id,
     }

    return render(request, 'accounts/Admin/Budget_Officer/preqform_bo.html', context)

   

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


def cdpurchase(request):
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
        'user': request.user
        
        
    }
    
    return render(request, 'accounts/Admin/Campus_Director/cdpurchase.html', context)

def preqform_cd(request, pr_id):
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
            cd_status=new_status,
            cd_comment=comment_content
        )

        return redirect('cdpurchase')

    elif request.method == 'GET':
        checkouts = get_object_or_404(Checkout, pr_id=pr_id)
        checkout_items = CheckoutItems.objects.filter(checkout=checkouts)
        context = {
            'checkouts': checkouts,
            'checkout_items': checkout_items,
            'pr_id': pr_id,
     }

    return render(request, 'accounts/Admin/Campus_Director/preqform_cd.html', context)
       

def update_cd_checkout_status(request, pr_id):
    if request.method == 'POST':
        try:
            new_status = request.POST.get("new_status")
            new_status = new_status.lower() == 'true' if isinstance(new_status, str) else new_status

            checkout = get_object_or_404(Checkout, pr_id=pr_id)
            checkout.date_updated = timezone.now()
            checkout.cd_seen = True
            checkout.cd_approve = new_status

            checkout.save()

            return redirect(reverse('preqform_cd', kwargs={'pr_id': pr_id}))
        except Checkout.DoesNotExist:
            return HttpResponse("CD Checkout not found.")
        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse("An error occurred while processing the CD form.")
    else:
        return HttpResponse("Invalid request method.")

  

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

def checkout_items_view(request):
    checkout_items = CheckoutItems.objects.all()
    context = {'checkout_items': checkout_items}
    return render(request, 'attachment/checkout_items.html', context)


def request_view(request):
    if request.method == 'POST':
        form = PurchaseRequestForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Your additional logic here
            return redirect('success_page')  # Redirect to a success page or another view
    else:
        form = PurchaseRequestForm()

    context = {'form': form}
    return render(request, 'history.html', context)
