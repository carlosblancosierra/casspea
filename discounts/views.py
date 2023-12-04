from django.shortcuts import redirect
from .models import Discount
from orders.models import Order
from carts.models import Cart
from django.contrib import messages


def validate_discount(request):
    if request.method == 'POST':
        discount_code = request.POST.get('discount_code')

        if discount_code:
            discount = Discount.objects.filter(code__iexact=discount_code, active=True).first()
            if discount:
                # Check if the user has already used the discount the maximum number of times
                if request.user.is_authenticated:
                    user = request.user
                    previous_orders = Order.objects.filter(user=user, discount=discount, payment_status="paid")
                    print(previous_orders)
                    if previous_orders.count() >= discount.max_uses:
                        discount_error = 'You have reached the maximum number of uses for this discount.'
                        request.session['discount_error'] = discount_error
                        return redirect('carts:home')  # RedirectRedirect to the cart page with an error message

                # Add the discount object to the session
                cart, created = Cart.objects.new_or_get(request)
                cart.discount = discount
                cart.save()
            else:
                discount_error = "Discount code not available"
                request.session['discount_error'] = discount_error

    return redirect('carts:home')  # Redirect to the cart page


def remove_discount(request):
    if request.method == 'POST':
        cart, created = Cart.objects.new_or_get(request)
        cart.discount = None
        cart.save()

    return redirect('carts:home')
