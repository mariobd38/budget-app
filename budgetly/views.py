from distutils.log import error
from django.shortcuts import render
from users.models import Users
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login,authenticate

def home_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user_obj = None
        user = None
        context = {
                "error":"Email address or password is incorrect"
        }
        try:
            user_obj = Users.objects.get(email=email)
            
            if user_obj.password == password:
                user = authenticate(request,email=email,password=password)

                # user = authenticate(request,email=email,password=password) 
            else:
                return render(request,"home.html",context=context)
        except:
            return render(request,"home.html",context=context)
        
        # user_obj_filter = Users.objects.filter(email=email)
        # print("FILTER:",user_obj_filter)
        
        # print("id",user_obj.id)
        # print("first name",user_obj.first_name)
        # print("last name",user_obj.last_name)
        # print("email",user_obj.email)
        # print("password",user_obj.password)
        
        context = {
            "object":user_obj,
        }
        print(user_obj)
        if user_obj is not None:
            auth_login(request,user) 
            return render(request,"user/home.html",context=context)


    return render(request,"home.html",{})

def login(request):
    pass

def create_account(request):
    context = {
        "password_length": 8,
        "lower_case": 1,
        "upper_case": 1,
        "numbers": 1,
    }
    if request.method=="POST":
        first_name = request.POST.get("f_name")
        last_name = request.POST.get("l_name")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm-password")
        email = request.POST.get("email")
        
        num_results = Users.objects.filter(email = email).count()
        if num_results > 0:
            context = {
                "email_error": "Email already exists"
            }
            return render(request,"register.html",context=context)

        
        password_context = password_validation(password,confirm_password)
        if(password_context is not None):
            return render(request,"register.html",password_context)
        username = email.split("@")[0]

        user_object = Users.objects.create(first_name=first_name,last_name=last_name,email=email,password=password)
        user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name, email=email,password=password)
        user.save()
        user_object = Users.objects.get(email=email)

        context = {
            "object":user_object
        }

        if user_object is not None:
            auth_login(request,user)
            return render(request,"user/home.html",context=context)

        
    return render(request,"register.html",context=context)

def admin_view(request):
    if request.method=="POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # superuser = authenticate(email=email)
        context = {
            "error":"Email or password is incorrect"
        }
        try:
            superuser = User.objects.get(email=email)
            if superuser.password != password or superuser is None:
                return render(request,"admin/sign_in.html",context=context)
        except:
            return render(request,"admin/sign_in.html",context=context)
        all_users = Users.objects.all()
        context = {
            "users":all_users
        }
        # print(all_users)

        return render(request,"admin/home.html",context=context)
    return render(request,"admin/sign_in.html",{})

def password_validation(password,confirm_password):
    context = {}
    errorDict = {}
    errorDict["password_not_matching"] = False
    errorDict["password_not_long"] = False
    errorDict["password_no_lc"] = False
    errorDict["password_no_uc"] = False
    errorDict["password_no_digit"] = False
    if password != confirm_password:
        errorDict["password_not_matching"] = True
        # errorList.append("Passwords, do not match")
    if len(password) < 8:
        errorDict["password_not_long"] = True
        # errorList.append("Password must be at least 8 characters longer")
    lower_case_count = sum(1 for c in password if c.islower())
    print("lower cases:",lower_case_count)
    if lower_case_count < 1:
                errorDict["password_no_lc"] = True
        # errorList.append("Password must contain a lower-case letter")
    upper_case_count = sum(1 for c in password if c.isupper())
    if upper_case_count < 1:
        errorDict["password_no_uc"] = True
        # errorList.append("Password must contain an upper-case letter")
    digit_count = sum(1 for c in password if c.isdigit())
    if digit_count < 1:
        errorDict["password_no_digit"] = True
        # errorList.append("Password must contain a number")
    for ed in errorDict:
        if errorDict.get(ed) == 'True':
            return {"error": errorDict}
    return None

