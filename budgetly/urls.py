"""budgetly URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
    home_view,
    create_account,
    admin_view,
)
from users.views import (
    user_home_view
)

urlpatterns = [
    path('user',user_home_view),
    path('',home_view),
    path('register/',create_account),
    path('admin/', admin.site.urls),
    path('admins/',admin_view), 
    path('', include("django.contrib.auth.urls"))
]
