from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from .models import Seller, Customer
from .middleware import SellerVerificationMiddleware
import random, json, re

User = get_user_model()

def validate_strong_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one digit.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError("Password must contain at least one special character.")
    
    
def seller_registration_view(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        shop_name = request.POST.get('shop_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        business_license = request.POST.get('business_license')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'registration.html', {'error': 'Password and confirm password do not match.'})
        
        try:
            validate_strong_password(password1)
        except ValidationError as e:
            return render(request, 'registration.html', {'error': e.message})
        
        # Generate a random OTP
        otp = random.randint(100000, 999999)
        
        # Send OTP via email
        subject = 'OTP for Seller Registration'
        message = f'Your OTP for seller registration is: {otp}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        
        send_mail(subject, message, email_from, recipient_list)
        
        # Store the OTP and user data in the session
        request.session['otp'] = otp
        request.session['user_data'] = {
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
            'shop_name': shop_name,
            'phone_number': phone_number,
            'email': email,
            'business_license': business_license,
            'password1': password1,
        }
        
        # Redirect to OTP verification page
        return redirect('verify_otp')
    
    return render(request, 'accounts/seller_registration.html')

def verify_otp_view(request):
    if request.method == "POST":
        otp1 = request.POST.get('otp1')
        otp2 = request.POST.get('otp2')
        otp3 = request.POST.get('otp3')
        otp4 = request.POST.get('otp4')
        otp5 = request.POST.get('otp5')
        otp6 = request.POST.get('otp6')

        user_otp = otp1 + otp2 + otp3 + otp4 + otp5 + otp6
        print(user_otp)
        stored_otp = request.session.get('otp')
        print(stored_otp)
        if int(user_otp) == stored_otp:
            print('ok')
            # OTP is correct, create the user and seller
            user_data = request.session.get('user_data')
            
            user, created = User.objects.get_or_create(
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                username=user_data['username'],
                email=user_data['email']
            )
            user.set_password(user_data['password1'])
            user.save()
            print('seller')
            seller = Seller.objects.create(
                user=user,
                shop_name=user_data['shop_name'],
                phone_number=user_data['phone_number'],
                business_license=user_data['business_license']
            )
            seller.is_active = True
            seller.save()
            
            # Clear the session data
            del request.session['otp']
            del request.session['user_data']
            
            return redirect('login')
        else:
            return render(request, 'accounts/verify_otp.html', {'error': 'Invalid OTP. Please try again.'})
    
    return render(request, 'accounts/verify_otp.html')

def seller_login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        #defind username by email
        try:
            username = User.objects.get(email=email).username
        except ObjectDoesNotExist:
            return render(request, 'accounts/seller_login.html',{'error': 'No user found with this email.'})

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Check if the user is associated with a Seller profile
            try:
                seller = Seller.objects.get(user=user)
                if seller.is_active:
                    # Log the user in
                    login(request, user)
                    return redirect('seller_dashboard')  
                else:
                    return render(request, 'accounts/seller_login.html',{'error': 'Your account is not active. Please contact support.'})
            except Seller.DoesNotExist:
                return render(request, 'accounts/seller_login.html',{'error': 'You are not registered as a seller.'})
        else:
            return render(request, 'accounts/seller_login.html',{'error':  'Invalid password.'})

    return render(request, 'accounts/seller_login.html')

def seller_logout(request):
    # Example: Log seller activity before logging out
    if hasattr(request.user, 'seller'):
        seller = request.user.seller
        print(f"Seller {seller.shop_name} has logged out.")
    
    logout(request)  # Logs out the user
    return redirect('home')

@SellerVerificationMiddleware
def seller_dashboard_view(request):
    seller = Seller.objects.get(user=request.user)

    return render(request, 'accounts/seller_dashboard.html', {
        'seller_name': f'{seller.user.first_name} {seller.user.last_name}',
        'shop_name':seller.shop_name.upper,

    })


def is_valid_email(email):
    if email is None:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def is_valid_username(username):
    pattern = r'^[a-zA-Z0-9_]{3,20}$'
    return re.match(pattern, username) is not None




def customer_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        f_name = str(data.get('fname'))
        l_name = str(data.get('lname'))
        username = str(data.get('username'))
        email = str(data.get('email'))
        password1 = str(data.get('password1'))
        password2 = str(data.get('password2'))
        phone_number = str(data.get('number'))

        # Validation checks
        if password1 != password2:
            return JsonResponse({'status': 'error', 'message': 'Passwords do not match.'})

        if User.objects.filter(username=username).exists():
            return JsonResponse({'status': 'error', 'message': 'Username is already taken.'})

        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'message': 'Email is already registered.'})

        # Create user and customer
        user = User.objects.create_user(
            username=username, 
            email=email, 
            password=password1,
            first_name=f_name,
            last_name=l_name
        )
        Customer.objects.create(user=user, phone_number=phone_number)

        # Log the user in
        login(request, user)

        return JsonResponse({'status': 'success', 'message': 'Registration successful!'})

def customer_login(request):
    domain = request.get_host()
    if request.method == 'POST':
        text = request.POST.get('username')
        password = request.POST.get('password')

        if is_valid_email(text):
            message = "email"
            try:
                username = User.objects.get(email=text).username
            except User.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': 'Invalid email'})
        else:
            username = text
            message = "username"

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 'success', 'message': 'Login successful', 'redirect_url': f'http://{domain}/'})
        else:
            return JsonResponse({'status': 'error', 'message': f'Invalid {message} or password'})

    return render(request, 'accounts/customer_auth.html', {"domain": domain})

def customer_logout(request):
    logout(request)
    return redirect('authentication')