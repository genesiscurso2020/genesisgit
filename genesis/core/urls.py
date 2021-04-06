from django.urls import path
from .views import CorePageView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

core_patterns = ([
    path('', CorePageView.as_view(), name='home'),
], 'core')