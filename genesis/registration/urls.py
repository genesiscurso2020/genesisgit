from django.urls import path
from .views import RegistroView, ProfileUpdateView, EmailUpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

registration_patterns = ([
    path('registro/', RegistroView.as_view(), name='registro'),
    path('profile/', login_required(ProfileUpdateView.as_view()), name='profile'),
    path('profile/email/', login_required(EmailUpdateView.as_view()), name='profile_email'),
], 'registration')