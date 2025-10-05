from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product, Order, OrderItem

def index(request):
    products = Product.objects.all()

    orders = []
    if request.user.is_authenticated:
        # show only THIS user's paid orders
        orders = Order.objects.filter(user=request.user, status=Order.STATUS_PAID).order_by('-created_at')

    return render(request, 'shop/index.html', {
        'products': products,
        'orders': orders,
        'STRIPE_PUBLISHABLE_KEY': '',  # unused for mock
    })


@require_POST
def create_checkout_session(request):
    """
    Simulated checkout: mark order as PAID immediately for demo.
    """
    if not request.user.is_authenticated:
        return redirect("login")  # force login before checkout

    # parse quantities from form
    items = []
    for key, val in request.POST.items():
        if key.startswith('qty_'):
            try:
                product_id = int(key.split('_', 1)[1])
                qty = int(val) if val else 0
            except ValueError:
                continue
            if qty > 0:
                try:
                    p = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    continue
                items.append((p, qty))

    if not items:
        return redirect('shop:index')

    # Create a new order
    order = Order.objects.create(user=request.user, status=Order.STATUS_PENDING)

    # Add items
    for product, qty in items:
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=qty,
            price_cents=product.price_cents
        )

    # Simulate payment success
    with transaction.atomic():
        order.status = Order.STATUS_PAID
        order.save()

    return redirect('shop:index')


# --- Authentication (Signup) ---
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login
            return redirect('shop:index')
    else:
        form = UserCreationForm()
    return render(request, "shop/signup.html", {"form": form})

