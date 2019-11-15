from django.shortcuts import render, redirect , get_object_or_404
from django.template import loader
from django.utils import timezone
from django.views.generic import ListView, DetailView, View
# Create your views here.
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, CheckoutForm, AccountForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from .models import Item , OrderItem, Order, Profile, Address, Payment
from django.views.generic.detail import SingleObjectMixin

import random
import string

def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=20))


def products(request):
    context = {
        'items': Item.objects.all()
    }
    return render(request, "products.html", context)

def is_valid_form(values):
    valid = True
    for field in values:
        if field == '':
            valid = False
    return valid

class CheckoutView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = CheckoutForm()
            profile = Profile.objects.get(user=self.request.user)
            context = {
                'form': form,
                'order': order,
                'profile': profile,

            }

            shipping_address_qs = Address.objects.filter(
                user=self.request.user,
                default=True
            )
            if shipping_address_qs.exists():
                context.update(
                    {'default_shipping_address': shipping_address_qs[0]})
            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have an active order")
            return redirect("user:checkout")

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            userprofile = Profile.objects.get(user=self.request.user)
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():

                use_default_shipping = form.cleaned_data.get(
                    'use_default_shipping')
                if use_default_shipping:
                    print("Using the defualt shipping address")
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True
                    )
                    if address_qs.exists():
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(
                            self.request, "No default shipping address available")
                        return redirect('user:checkout')
                else:
                    print("User is entering a new shipping address")
                    shipping_address1 = form.cleaned_data.get(
                        'shipping_address')


                    if is_valid_form([shipping_address1]):
                        shipping_address = Address(
                            user=self.request.user,
                            street_address=shipping_address1,
                        )
                        shipping_address.default = True
                        shipping_address.save()

                        order.shipping_address = shipping_address
                        order.save()



                    else:
                        messages.info(
                            self.request, "Please fill in the required shipping address fields")
                #total amount
                # amount = int(order.get_total() * 100)
                userprofile.one_click_purchasing = True
                userprofile.name_profile = form.cleaned_data.get('name_profile')
                userprofile.numberphone = form.cleaned_data.get('numberphone')
                userprofile.save()


                # create the payment
                payment = Payment()
                payment.user = self.request.user
                payment.amount = order.get_total()
                payment.save()

                order_items = order.items.all()
                order_items.update(ordered=True)
                for item in order_items:
                    item.save()

                order.ordered = True
                order.payment = payment
                order.ref_code = create_ref_code()
                order.save()

                messages.success(self.request, "Your order was successful!")
                return redirect("user:home")


        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an active order")
            return redirect("user:checkout")


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
            return redirect("user:checkout")
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
            messages.info(request, "This item was removed from your cart.")
            return redirect("user:checkout")
        else:
            messages.info(request, "This item was not in your cart")
            return redirect("user:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order")
        return redirect("user:product", slug=slug)


class Account(DetailView):
    """docstring for Account."""
    model = Profile
    def get(self, *args, **kwargs):

        order = Order.objects.filter(user=self.request.user, ordered=True)
        payment = Payment.objects.filter(user = self.request.user)
        form = AccountForm()
        context = {
            'order':order,
            'payment':payment,
            'form':form,

        }
        template_name = "account.html"
        return render(self.request,'account.html' ,context)
    def post(self, *args, **kwargs):
        form = AccountForm(self.request.POST or None)
        try:
            userprofile = Profile.objects.get(user=self.request.user)
            userprofile.name_profile = form.cleaned_data.get('name_profile')
            userprofile.numberphone = form.cleaned_data.get('numberphone')
            userprofile.save()

            shipping_address1 = form.cleaned_data.get(
                'shipping_address')
            shipping_address = Address(
                user=self.request.user,
                street_address=shipping_address1,
            )
            shipping_address.save()
        except ObjectDoesNotExist:
            messages.warning(self.request, "You do not have an profile")
            return redirect('account.html')

    # def get_object(self):
    #     return get_object_or_404(User, slug = self.request.user)
    # def get_object(self):
    #     """Return's the current users profile."""
    #     return self.request.user.username


class HomeView(ListView):
    #this class return for home site
    model = Item
    paginate_by = 10
    template_name = "home.html"

class ItemDetailView(DetailView):
    #this class return for product site
    #model la nhung thu ma product site nay duoc cung cap boi model.py
    model = Item
    template_name = "product.html"
