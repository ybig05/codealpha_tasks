# store/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category, Order, OrderItem
from .cart import Cart
from .forms import RegisterForm, CheckoutForm


# ── Product listings ────────────────────────────────────────────────────────

def home(request):
    products   = Product.objects.filter(available=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'store/home.html',
                  {'products': products, 'categories': categories})


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'store/product_detail.html', {'product': product})


# ── Cart ────────────────────────────────────────────────────────────────────

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


def cart_add(request, product_id):
    product  = get_object_or_404(Product, id=product_id)
    cart     = Cart(request)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(product, quantity=quantity)
    messages.success(request, f'"{product.name}" added to cart.')
    return redirect('cart_detail')


def cart_remove(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Cart(request).remove(product)
    return redirect('cart_detail')


# ── Checkout & Orders ───────────────────────────────────────────────────────

@login_required
def checkout(request):
    cart = Cart(request)
    if not cart.cart:
        messages.warning(request, 'Your cart is empty.')
        return redirect('home')
    form = CheckoutForm()
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(
                user        = request.user,
                full_name   = form.cleaned_data['full_name'],
                email       = form.cleaned_data['email'],
                address     = form.cleaned_data['address'],
                city        = form.cleaned_data['city'],
                country     = form.cleaned_data['country'],
                postal_code = form.cleaned_data['postal_code'],
            )
            for item in cart:
                OrderItem.objects.create(
                    order    = order,
                    product  = item['product'],
                    quantity = item['quantity'],
                    price    = item['price'],
                )
                # Deduct stock
                product = item['product']
                product.stock -= item['quantity']
                product.save()
            cart.clear()
            messages.success(request, 'Order placed successfully!')
            return redirect('order_success', order_id=order.id)
    return render(request, 'store/checkout.html', {'cart': cart, 'form': form})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/order_success.html', {'order': order})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/my_orders.html', {'orders': orders})


# ── Auth ────────────────────────────────────────────────────────────────────

def register_view(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created! Welcome.')
            return redirect('home')
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user     = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect(request.GET.get('next', 'home'))
        messages.error(request, 'Invalid username or password.')
    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')