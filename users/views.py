from django import views
from django.shortcuts import render
import budgetly.views as main
import datetime
# Create your views here.
def user_home_view(request):
    now = datetime.datetime.now()
    context = {
        "time": now
    }
    return render(request,"user/home.html",context=context)