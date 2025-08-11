from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
# Create your views here.
def home(request):
    return render(request,'blog.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')

        if not all([first_name, last_name, username, email, password]):
            messages.error(request, "Please fill in all the fields.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username is already taken.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')

        user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
        return redirect('login')
    return render(request,'accounts/register.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')
    return render(request,'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# def forgot_password(request):

