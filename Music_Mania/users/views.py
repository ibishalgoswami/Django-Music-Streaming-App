from django.shortcuts import render
from django.views import View
from django.template.response import TemplateResponse
from django.views.generic import TemplateView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.conf import settings
from django.core.mail import send_mail
import requests
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from .models import *
from datetime import datetime


from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage 
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

UserModel = get_user_model()





# Create your views here.

class UserRegistrationPageView(View):
    template_name = "signup.html"
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect('/')
        else:
            response = TemplateResponse(request, self.template_name)
            return response


class UserRegistrationhandle(TemplateView):
    template_name = "signup.html"
    
    def post(self, request, *args, **kwargs):
        username = self.request.POST.get('username')
        email = self.request.POST.get('email')
        password= self.request.POST.get('password')

        if User.objects.filter(username=username).exists():
            return self.render_to_response({'error':'Username already exists'}) 
        else:
            # captcha verification
            secret_key = settings.RECAPTCHA_SECRET_KEY
            client_screat=self.request.POST.get('g-recaptcha-response')
            data = {
                'response': client_screat,
                'secret': secret_key
            }
            resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result_json = resp.json()
            print(result_json)
            if not result_json.get('success'):
                return self.render_to_response({'error':'Captcha not verified'})
            # end captcha verification

            else:
                user = User.objects.create_user(username, email, password)
                user.is_active = False  # Deactivate account till it is confirmed
                user.save()
                current_site = get_current_site(request)
                mail_subject = 'Activate your account.'
                message = render_to_string('account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                to_email = self.request.POST.get('email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                return self.render_to_response({'msg':'Sign up Done. Please confirm your email address to complete the registration'})


class UserLoginHandle(View):    
    def post(self, request):
        username = self.request.POST.get('username')
        password= self.request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            messages.success(self.request, 'Login successful')
            #user logs start here
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ipaddress = x_forwarded_for.split(',')[-1].strip()
            else:
                ipaddress = request.META.get('REMOTE_ADDR')
            get_ip= LoginLogoutLog(user=request.user,ip_address=ipaddress,login_time=datetime.now()) #imported class from model
            # get_ip.ip_address= ipaddress
            # get_ip.pub_date = datetime.date.today() #import datetime
            get_ip.save()
            #user logs ends here
        else:
            messages.error(self.request, 'Login Failed')
        return HttpResponseRedirect('/')


class UserLogoutHandle(View):    
    def get(self, request):
        logout(request)
        # get_logout_time=datetime.now()
        # user_logout_time=LoginLogoutLog()
        # user_logout_time.logout_time=get_logout_time
        # user_logout_time.save()

        messages.success(self.request, 'You are logged out')
        return HttpResponseRedirect('/')


class ActivateAccount(TemplateView):
    template_name = "thankyou.html"
    
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return self.render_to_response({'msg':'Thank you for your email confirmation. Now you can login your account.'})
        else:
            return HttpResponse('Activation link is invalid!')
            return self.render_to_response({'msg':'Activation link is invalid!'})
