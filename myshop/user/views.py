from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
# Create your views here.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Item


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             user.refresh_from_db()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Your account has been created! You are now able to log in')
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'register.html', {'form': form})

def register(request):
    if request.method == 'POST':
        if 'registerbtn' in request.POST:
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.refresh_from_db()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Your account has been created! You are now able to log in')
                return render(request, 'register.html', {'form': form})
        elif 'loginbtn' in request.POST:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username = username, password = password)
            if user is not None:
                form = login(request, user)
                messages.success(request, f' wecome {username} !!')
                return redirect('user:home')
            else:
                messages.info(request, f'account done not exit plz sign in')
                form = AuthenticationForm()
            return render(request, 'register.html', {'form': form})
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# def home(request):
#     my_dict = {'content':'Home page'}
#     return render(request,'home.html',context = my_dict)

# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "products.html", context)

class HomeView(ListView):
    model = Item
    paginate_by = 10
    template_name = "home.html"

class ItemDetailView(DetailView):
    model = Item
    template_name = "product.html"
