from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from .forms import LeaveRequestForm
from .models import LeaveRequest

# Create your views here.
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