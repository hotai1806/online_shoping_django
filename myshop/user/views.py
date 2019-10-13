from django.shortcuts import render, redirect
from django.template import loader
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
# Create your views here.

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

from .models import Item


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
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
