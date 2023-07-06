from django.shortcuts import redirect
from .models import Discount
from orders.models import Order
from carts.models import Cart


def validate_discount(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code')

        if discount_code:
            discount = Discount.objects.filter(code__icontains=discount_code).first()
            if discount:
                # Check if the user has already used the discount the maximum number of times
                user = request.user
                previous_orders = Order.objects.filter(user=user, discount=discount, payment_status="paid")
                if previous_orders.count() >= discount.max_uses:
                    message = 'You have reached the maximum number of uses for this discount.'
                    return redirect('carts:home')  # Redirect to the cart page with an error message

                # Add the discount object to the session
                cart, created = Cart.objects.new_or_get(request)
                cart.discount = discount
                cart.save()

    return redirect('carts:home')  # Redirect to the cart page


def remove_discount(request):
    if request.method == 'POST':
        cart, created = Cart.objects.new_or_get(request)
        cart.discount = None
        cart.save()

    return redirect('carts:home')
