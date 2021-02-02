from django.urls import path,include
from .views import *

urlpatterns = [
    path('', UserRegistrationPageView.as_view()),
    path('create_account', UserRegistrationhandle.as_view()),
    path('login', UserLoginHandle.as_view()),
    path('logout', UserLogoutHandle.as_view()),
    path('activate/<uidb64>/<token>/',ActivateAccount.as_view(), name='activate'),
    
]