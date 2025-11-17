from .models import Application
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegisterForm, UserLoginForm, ApplicationForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# ЗАДАНИЕ 1

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})

# ЗАДАНИЕ 2

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def create_application(request):
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    return render(request, 'create_application.html', {'form': form})

@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).order_by('-created_at')
    status = request.GET.get('status')
    if status in ['new', 'in_progress', 'completed']:
        applications = applications.filter(status=status)

    return render(request, 'my_applications.html', {
        'applications': applications,
        'current_status': status,
        'STATUS_CHOICES': Application.STATUS_CHOICES,
    })

@login_required
def delete_application(request, pk):
    app = get_object_or_404(Application, pk=pk, user=request.user)
    if app.status != 'new':
        return redirect('my_applications')

    if request.method == 'POST':
        app.delete()
        return redirect('my_applications')

    return render(request, 'confirm_delete.html', {'application': app})


# ЗАДАНИЕ 3

@staff_member_required
def admin_applications(request):
    applications = Application.objects.all().order_by('-created_at')
    return render(request, 'admin_applications.html', {
        'applications': applications,
    })

from django.contrib.admin.views.decorators import staff_member_required
from .forms import AdminApplicationForm

@staff_member_required
def edit_application(request, pk):
    app = get_object_or_404(Application, pk=pk)

    if request.method == 'POST':
        form = AdminApplicationForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('admin_applications')
    else:
        form = AdminApplicationForm(instance=app)

    return render(request, 'edit_application.html', {
        'form': form,
        'application': app,
    })