from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import Client, UserProfile, CpdInfo
from .forms import ClientForm, UserCreationFormWithClient, UserEditForm, CpdInfoForm

# General
def index(request):
    return render(request, "home/index.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            # stay on login page silently (no message)
            return render(request, "home/login.html")

    return render(request, "home/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def dashboard_view(request):
    cpd_info = CpdInfo.objects.filter(user=request.user.id)
    return render(request, "home/dashboard.html", {"cpd_info": cpd_info})

def add_new(request):
    if request.method == "POST":
        form = CpdInfoForm(request.POST)
        if form.is_valid():
            cpd = form.save(commit=False)
            cpd.user = request.user
            cpd.save()
            return redirect("dashboard")
    else:
        form = CpdInfoForm()

    return render(request, 'home/add_new.html', {"form": form})

# CLIENTS
def client_list(request):
    clients = Client.objects.all()
    return render(request, "home/client_list.html", {"clients": clients})

def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("client_list")  # name of the urlpattern for your list view
    else:
        form = ClientForm()

    return render(request, "home/client_create.html", {"form": form})

def client_read(request, client_id):
    client = Client.objects.get(id=client_id)
    return render(request, "home/client_read.html", {"client": client})

def client_update(request, client_id):
    client = get_object_or_404(Client, id=client_id)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            return redirect("client_list")  # go back to list after save
    else:
        form = ClientForm(instance=client)
    return render(request, "home/client_update.html", {"form": form, "client": client})

def client_delete(request, client_id):
    client = get_object_or_404(Client, id=client_id)
    
    if request.method == "POST":
        client.delete()
        return redirect("client_list")  # After deletion, go back to list
    return render(request, "home/client_delete.html", {"client": client})

# USERS
def user_list(request):
    profiles = UserProfile.objects.select_related('user', 'client').all()
    return render(request, "home/user_list.html", {"profiles": profiles})

def user_create(request):
    if request.method == 'POST':
        form = UserCreationFormWithClient(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')  # redirect to your list of users
    else:
        form = UserCreationFormWithClient()
    
    return render(request, 'home/user_create.html', {'form': form})

def user_read(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, "home/user_read.html", {"user": user})

def user_update(request, user_id):
    user = get_object_or_404(User, id=user_id)
    
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_list")  # adjust to your list view
    else:
        form = UserEditForm(instance=user)

    return render(request, "home/user_update.html", {"form": form, "user": user})

def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        user.delete()
        return redirect("user_list")

    return render(request, "home/user_delete.html", {"user": user})