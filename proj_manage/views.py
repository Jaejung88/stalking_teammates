from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.

def index(request):
    return render(request, "index.html")

def register(request):
    if request.method == "POST":
        user = User.objects.filter(email = request.POST["email"])
        if len(user) > 0:
            messages.error(request, "This email is already in use", extra_tags = "email")
            return redirect("/")
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val, extra_tags = key)
            return redirect("/")
        
        # need to hash pw after check all of the invalid information
        pw = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt()).decode()

        User.objects.create(
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            email = request.POST["email"],
            password = pw
        )

        request.session["user_id"] = User.objects.last().id
        return redirect("/dashboard")
    else:
        return redirect("/")

def dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "user": User.objects.get(id=request.session["user_id"]),
            "all_project": Project.objects.all()
        }
        return render(request, "dashboard.html", context)

def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val, extra_tags = key)
            return redirect("/")

        user = User.objects.filter(email = request.POST["login_email"])

        if not user:
            messages.error(request, "Invalid Email/Password", extra_tags = "login")
            return redirect("/")

        if not bcrypt.checkpw(request.POST["login_password"].encode(), user[0].password.encode()):
            messages.error(request, "Invalid Email/Password", extra_tags = "login")
            return redirect("/")

        request.session["user_id"] = user[0].id
        return redirect("/dashboard")
    else:
        return redirect("/")
    
def logout(request):
    if "user_id" in request.session:
        del request.session["user_id"]
    return redirect("/")

def show_user(request,user_id):
	context ={
		'user': User.objects.get(id=user_id)
	}

	return render(request,'show_user.html',context)

def edit_user(request):
	context = {
		'edit': User.objects.get(id=request.session['user_id']),
	}

	return render(request,'edit_user.html',context)

def update_user(request):
	if request.method == "POST":
		errors = User.objects.edit_validator(request.POST)
		if len(errors) > 0:
			for key, value in errors.items():
				messages.error(request,value,extra_tags=key)
			return redirect('/edit_user')
		
		update = User.objects.get(id=request.session['user_id'])
		update.first_name = request.POST['edit_first_name']
		update.last_name = request.POST['edit_last_name']
		update.email = request.POST['edit_email']
		update.save()
		return redirect('/dashboard')
	else:
		return redirect('/logout')

def create_project(request):
    if request.method == "POST":
        errors = Project.objects.project_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect("/dashboard")

        Project.objects.create(
            project_name = request.POST["project_name"],
            project_desc = request.POST["project_desc"],
            project_due_date = request.POST["project_due_date"],
            admin_user = User.objects.get(id=request.session["user_id"])
        )

        return redirect("/dashboard")
    else:
        return redirect("logout")

def project_page(request, project_id):
    return HttpResponse(f"This is a placeholder for project id:{project_id}. And it workd!")

def destroy_project(request, project_id):
	destroy = Project.objects.get(id=project_id)
	destroy.delete()
	return redirect('/dashboard')