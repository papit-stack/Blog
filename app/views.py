from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from .models import Category,Blog
from django.urls import reverse
from django.core.mail import EmailMessage
from django.utils import timezone
from .models import PasswordReset  
from django.conf import settings
from .forms import BlogForm
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

# Create your views here.
def home(request):
    category=Category.objects.all()
    blog=Blog.objects.filter(is_published=True).order_by('-created_at')
    context={'category':category,'blog':blog}
    return render(request,'blog.html',context)

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

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            reset_user_password = PasswordReset(user=user)
            reset_user_password.save()
            relative_url = reverse('reset-password', kwargs={'reset_id': reset_user_password.reset_id})
            absolute_url = request.build_absolute_uri(relative_url)
            email_body = f"Reset your password using the following link: {absolute_url}"
            email_message = EmailMessage(
                'Reset your password',
                email_body,
                settings.EMAIL_HOST_USER,
                [email]
            )
            email_message.fail_silently = False
            email_message.send()
            messages.success(request, "Password reset link sent to your email.")
            return redirect('forgot-password')
        else:
            messages.error(request, "Email not found.")
            return redirect('forgot-password')
    return render(request, 'accounts/forgot_password.html')

def reset_password(request, reset_id):
    reset_entry = get_object_or_404(PasswordReset, reset_id=reset_id)
    
    if request.method == "POST":
        password = request.POST.get('password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        # Check for empty password fields
        if not password or not confirm_password:
            messages.error(request, 'Password fields cannot be empty or just spaces.')
            return redirect('reset-password', reset_id=reset_id)

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('reset-password', reset_id=reset_id)

        # Check if reset link expired (assuming created_at is datetime field on PasswordReset model)
        expiration_time = reset_entry.created_at + timezone.timedelta(minutes=10)
        if timezone.now() > expiration_time:
            reset_entry.delete()  # Delete expired token
            messages.error(request, 'Reset link has expired.')
            return redirect('forgot-password')  # Or wherever you want to redirect on expiry

        # If all good, update user password and delete reset token
        user = reset_entry.user
        user.set_password(password)
        user.save()
        reset_entry.delete()
        messages.success(request, 'Password reset successfully. You can now log in.')
        return redirect('login')

    return render(request, 'accounts/reset_password.html', {'reset_id': reset_id})

@login_required
def add_post(request):
    if request.method=="POST":
        form=BlogForm(request.POST,request.FILES)
        if form.is_valid():
            blog=form.save(commit=False)
            blog.author=request.user
            if not blog.slug:
                slug_base=slugify(blog.blog_title)
                unique_slug=slug_base
                counter=1
                while Blog.objects.filter(slug=unique_slug).exists():
                    unique_slug=f"{slug_base}-{counter}"
                    counter+=1
                blog.slug=unique_slug
                blog.save()
                return redirect('home')
    else:
        form=BlogForm()
    context={'form':form}
    return render(request,'post.html',context)

def blog_detail(request,slug):
    blog=get_object_or_404(Blog,slug=slug,is_published=True)
    return render(request,'blog_detail.html',{'blog':blog})
