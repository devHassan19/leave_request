from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .forms import LeaveRequestForm , RegisterForm
from .models import LeaveRequest

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import RegisterForm

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user_type = form.cleaned_data.get("user_type")

            user = User.objects.create_user(username=username, password=password)

            user.is_staff = user_type == 'staff'
            user.save()

           
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
        
    return render(request, 'accounts/register.html', {'form': form})
            

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin-page/')
            elif user.is_staff:
                return redirect('/staff-page/')
            else:
                return redirect('/')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')


def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def staff_page(request):
    message = ''
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST, request.FILES)
        if form.is_valid():
            LeaveRequest.objects.create(
                user=request.user,
                leave_type=form.cleaned_data['leave_type'],
                attachment=form.cleaned_data['attachment']
            )
            message = 'Request submitted successfully!'
            form = LeaveRequestForm()
    else:
        form = LeaveRequestForm()

    user_leaves = LeaveRequest.objects.filter(user=request.user).order_by('-submitted_at')

    return render(request, 'accounts/staff_page.html', {
        'form': form,
        'message': message,
        'user_leaves': user_leaves,
    })

def is_superuser_user(user):
    return user.is_superuser

@login_required
@user_passes_test(is_superuser_user)
def admin_page(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        leave_id = request.POST.get('leave_id')
        leave = LeaveRequest.objects.get(id=leave_id)
        if action == 'approve':
            leave.status = 'Approved'
        elif action == 'reject':
            leave.status = 'Rejected'
        leave.save()
    leaves = LeaveRequest.objects.all().order_by('-submitted_at')
    return render(request, 'accounts/admin_page.html', {'leaves': leaves})


def logout_view(request):
     if request.method == "POST":
         logout(request)
         return redirect('login')
     else:
         return redirect('login')