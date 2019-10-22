from django.shortcuts import render, redirect , get_object_or_404
from django.template import loader
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, CheckoutForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Item , OrderItem, Order

def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)






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

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("user:product",slug = slug)
        else:
            order.items.add(order_item)
            messages.info(request, "This item was added to your cart.")
            return redirect("user:product",slug = slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "This item was added to your cart.")
        return redirect("user:product",slug = slug)


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            order.items.remove(order_item)
            messages.info(request, "This item was removed from your cart.")
            return redirect("user:product", slug=slug)
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("user:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("user:product", slug=slug)




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
