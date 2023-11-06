from django.shortcuts import render, redirect

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from django.contrib.auth import authenticate, login, logout

import datetime
from .models import Order, STATUS_CHOICES, CANCELED
from .emails import new_order_staff_mail

from carts.models import Cart, CartEntry
from addresses.models import Address
from shipping.models import ShippingType

import stripe

more_than_15_discount_id_test = 'kNMyLyWK'
more_than_15_discount_id_live = 'lk8ip9No'

more_than_30_discount_id_test = 'NUGvdvL1'
more_than_30_discount_id_live = 'ln6FgI7i'

if settings.STRIPE_TEST:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    more_than_15_discount_id = more_than_15_discount_id_test
    more_than_30_discount_id = more_than_30_discount_id_test
else:
    stripe.api_key = settings.STRIPE_SECRET_KEY_LIVE
    more_than_15_discount_id = more_than_15_discount_id_live
    more_than_30_discount_id = more_than_30_discount_id_live

endpoint_secret_local = 'whsec_6b5511c942d67d52e2096ba71873235922a895c8d0cd088e50b743cc396f5ed3'
endpoint_secret_test = 'whsec_ve12rsdRiGfusHPvdJM3BQJGlgo5T9N1'
endpoint_secret_live = 'whsec_FlObtoSReNkoxj5DCBIZ7L0JGlGTe1sC'


# Create your views here.

def address_page(request):
    # if not request.user.is_authenticated:
    #     return redirect('/login?next=/orders/address')

    entries = CartEntry.objects.entries(request)
    if not entries:
        return redirect("carts:home")

    guest = not request.user.is_authenticated
    addresses = None
    # address = None
    address_to_update = None

    address_id = request.session.get("address_id", None)
    if not guest:
        addresses = Address.objects.filter(user=request.user, active=True)
        address_qs = addresses.filter(id=address_id)

        address_to_update = None
        if len(address_qs) == 1:
            address_to_update = address_qs.first()
            addresses = addresses.exclude(id=address_id)

    context = {
        "title": 'Checkout',
        "addresses": addresses,
        "address": address_to_update,
    }

    form = request.POST
    if form:
        update_address_id = form.get('update_address_id', False)
        reuse_address_id = form.get('reuse_address_id', False)
        delete_address_id = form.get('delete_address_id', False)

        if update_address_id:
            address_qs = Address.objects.filter(id=address_id)
            full_name = form['full_name']
            street = form['street']
            postal_code = form['postal_code']
            city = form['city']
            tel = form['tel']
            country = form['country']
            address_qs_unique = len(address_qs) == 1

            all_variables = [address_qs_unique, full_name, street, postal_code, city, tel, country]

            if all(all_variables):
                address_qs.update(
                    full_name=full_name,
                    street=street,
                    postal_code=postal_code,
                    city=city,
                    tel=tel,
                    country=country,
                )

            request.session['address_id'] = form['update_address_id']
        elif reuse_address_id:
            request.session['address_id'] = reuse_address_id
        elif delete_address_id:
            Address.objects.filter(id=delete_address_id).update(active=False)
            return redirect('orders:address')
        else:
            full_name = form['full_name']
            street = form['street']
            postal_code = form['postal_code']
            city = form['city']
            tel = form['tel']
            country = form['country']

            address = Address(
                full_name=full_name,
                street=street,
                postal_code=postal_code,
                city=city,
                tel=tel,
                country=country,
                # user=request.user
            )
            address.save()

            if not guest:
                address.user = request.user

            request.session['address_id'] = address.id

        return redirect('orders:confirm')

    return render(request, "orders/address.html", context)


def confirm_page(request):
    cart, created = Cart.objects.new_or_get(request)

    if request.method == "POST":
        selected_shipping_type_id = request.POST.get('shipping_type')

        # Ensure that selected_shipping_type_id is a valid integer
        try:
            selected_shipping_type_id = int(selected_shipping_type_id)
        except ValueError:
            # Handle the case where the ID is not a valid integer
            # Redirect or show an error message as needed
            pass

        # Update the cart's selected shipping type (replace with your logic)
        cart.shipping_type_id = selected_shipping_type_id
        cart.save()

    address_id = request.session.get("address_id", None)
    gift_message = request.session.get("gift_message", None)
    shipping_date = request.session.get("shipping_date", None)

    entries = CartEntry.objects.entries(request)
    if not entries.exists():
        return redirect("carts:home")

    discount = cart.discount
    discount_total = CartEntry.objects.discount_total(request)
    total = cart.total
    subtotal = cart.subtotal

    shipping_types = ShippingType.objects.active()

    shipping_free = cart.shipping_free
    if shipping_free:
        shipping_cost = 0

    address = None
    address_qs = Address.objects.filter(id=address_id)
    if len(address_qs) == 1:
        address = address_qs.first()

    context = {
        "title": 'Checkout',
        "discount": discount,
        "discount_total": discount_total,
        "address": address,
        "entries": entries,
        "total": total,
        "shipping_free": shipping_free,
        "gift_message": gift_message,
        # "shipping_cost": shipping_cost,
        "shipping_date": shipping_date,
        "subtotal": subtotal,
        "shipping_types": shipping_types,
        "cart": cart,
    }

    return render(request, "orders/confirm.html", context)


class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        # create order
        cart_entries = CartEntry.objects.entries(request)
        address_id = request.session.get("address_id", None)
        gift_message = request.session.get("gift_message", None)
        shipping_address_qs = Address.objects.filter(id=address_id)
        shipping_address = None
        if len(shipping_address_qs) != 1:
            return redirect('carts:home')
        elif len(shipping_address_qs) == 1:
            shipping_address = shipping_address_qs.first()

        shipping_date = request.session.get("shipping_date", None)
        shipping_date_obj = None
        if shipping_date:
            shipping_date_obj = datetime.datetime.strptime(shipping_date, '%b %d, %Y')
            shipping_date_obj = shipping_date_obj.date()
        cart, created = Cart.objects.new_or_get(request)
        discount = cart.discount
        order = Order(shipping_address=shipping_address,
                      gift_message=gift_message,
                      shipping_date=shipping_date_obj,
                      discount=cart.discount,
                      shipping_type=cart.shipping_type
                      )
        customer_email = None
        if request.user.is_authenticated:
            order.user = request.user
            customer_email = request.user.email
        order.save()
        order.cart_entries.set(cart_entries)
        order_id = order.order_id

        # request.session['cart_id'] = None
        # request.session['address_id'] = None
        # request.session['gift_message'] = None
        request.session['order_id'] = order_id
        line_items = []
        for entry in cart_entries:
            line_items.append({
                'price': str(entry.product.get_price_id),
                'quantity': str(entry.quantity),
            })

        # send order id to stripe
        domain = "https://www.casspea.co.uk"
        if settings.STATIC_LOCAL:
            domain = "http://127.0.0.1:9000"

        shipping_free = {
            "shipping_rate_data": {
                "type": "fixed_amount",
                "fixed_amount": {"amount": 0, "currency": "gbp"},
                "display_name": "Free shipping",
                # "delivery_estimate": {
                #     "minimum": {"unit": "business_day", "value": 5},
                #     "maximum": {"unit": "business_day", "value": 7},
                # },
            },
        }

        shipping_type = cart.shipping_type

        shipping_basic = {
            "shipping_rate_data": {
                "type": "fixed_amount",
                "fixed_amount": {"amount": shipping_type.cents, "currency": "gbp"},
                "display_name": shipping_type.name,
                # "delivery_estimate": {
                #     "minimum": {"unit": "business_day", "value": 5},
                #     "maximum": {"unit": "business_day", "value": 7},
                # },
            },
        }

        shipping_options = [shipping_basic]
        if order.shipping_free:
            shipping_options = [shipping_free]

        invoice_creation = {
            "enabled": True,
            "invoice_data": {
                "description": "CassPea.co.uk Invoice",
                "metadata": {"order": order_id},
                # "account_tax_ids": [],
                # "custom_fields": [{"name": "Purchase Order", "value": "PO-XYZ"}],
                # "rendering_options": {"amount_tax_display": "include_inclusive_tax"},
                "footer": "CassPea",
            },
        }
        if discount:
            discounts = [{'coupon': discount.stripe_id}]
        else:
            discounts = []

        allow_promotion_codes = False
        # if CartEntry.objects.more_than_30(request):
        #     discounts = [{'coupon': more_than_30_discount_id}]
        #     allow_promotion_codes = False
        # elif CartEntry.objects.more_than_15(request):
        #     discounts = [{'coupon': more_than_15_discount_id}]
        #     allow_promotion_codes = False

        if not allow_promotion_codes:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                customer_email=customer_email,
                currency='GBP',
                mode='payment',
                discounts=discounts,
                shipping_options=shipping_options,
                client_reference_id=order_id,
                success_url=domain + '/orders/success',
                cancel_url=domain + '/orders/cancel',
                invoice_creation=invoice_creation,
            )
        else:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                customer_email=customer_email,
                currency='GBP',
                mode='payment',
                shipping_options=shipping_options,
                client_reference_id=order_id,
                success_url=domain + '/orders/success',
                cancel_url=domain + '/orders/cancel',
                allow_promotion_codes=allow_promotion_codes,
                invoice_creation=invoice_creation,
            )

        return redirect(checkout_session.url)


@csrf_exempt
def my_webhook_view(request):
    payload = request.body
    # if settings.STATIC_LOCAL:
    #     endpoint_secret = endpoint_secret_local

    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    endpoint_secret = endpoint_secret_test
    if not settings.STRIPE_TEST:
        endpoint_secret = endpoint_secret_live
    elif settings.STATIC_LOCAL:
        endpoint_secret = endpoint_secret_local

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

        # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
        )

        # set order to paid
        order_id = session['client_reference_id']
        order_obj_qs = Order.objects.filter(order_id=order_id)
        if len(order_obj_qs) != 1:
            messages.error('Order Error')
            return redirect('carts:home')
        order = order_obj_qs.first()
        order.stripe_data = session
        order.payment_status = session['payment_status']
        order.save()

        # order_entries = order.cart_entries.all()
        # if len(order_entries) > 0:
        #     cart = order_entries.first().cart
        #     cart.active = False
        #     cart.save()

    return HttpResponse(status=200)


def success_page(request):
    order_id = request.session.get('order_id', None)
    new_order_staff_mail(request, order_id)
    order_qs = Order.objects.filter(order_id=order_id)
    if len(order_qs) == 1:
        order = order_qs.first()

    else:
        return redirect('carts:home')

    request.session['cart_id'] = None
    request.session['address_id'] = None
    request.session['gift_message'] = None

    import json
    data = json.loads(order.stripe_data)

    # Extract payment_intent and amount_total
    transaction_id = data.get('payment_intent')
    total_revenue = data.get('amount_total')

    context = {
        "order": order,
        "address": order.shipping_address,
        "entries": order.cart_entries.all,
        "gift_message": order.gift_message,
        "shipping_cost": order.shipping_cost,
        'transaction_id': transaction_id,
        'total_revenue': total_revenue
    }

    return render(request, "orders/created.html", context)


def cancel_page(request):
    order_id = request.session.get('order_id', None)
    order_qs = Order.objects.filter(order_id=order_id)
    if len(order_qs) == 1:
        order = order_qs.first()
    else:
        return redirect('carts:home')

    order.stats = "CANCELED"
    order.save()
    request.session['order_id'] = None

    return redirect("carts:home")


@staff_member_required
def staff_list_page(request):
    order_qs = Order.objects.filter(payment_status="paid")

    paginator = Paginator(order_qs, 50)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "orders": page_obj,
    }

    return render(request, "orders/staff-list.html", context)


@staff_member_required
def staff_detail_page(request, order_id):
    order = None
    order_qs = Order.objects.filter(order_id=order_id)
    if len(order_qs) == 1:
        order = order_qs.first()

    if request.POST:
        form = request.POST
        status = form.get('order-status')
        if order:
            order.status = status
            order.save()
            messages.success(request, 'Order status updated')

    context = {
        "order": order,
        "address": order.shipping_address,
        "entries": order.cart_entries.all,
        "STATUS_CHOICES": STATUS_CHOICES,
    }

    return render(request, "orders/staff-detail.html", context)


@login_required
def detail_page(request, order_id):
    order = None
    order_qs = Order.objects.filter(order_id=order_id)

    if len(order_qs) == 1:
        order = order_qs.first()

    if order.user != request.user:
        return HttpResponseForbidden()

    context = {
        "order": order,
        "address": order.shipping_address,
        "entries": order.cart_entries.all,
    }

    return render(request, "orders/detail.html", context)


@login_required
def list_page(request):
    order_qs = Order.objects.filter(user=request.user)

    context = {
        "orders": order_qs,
    }

    return render(request, "orders/list.html", context)


@staff_member_required
def email_test(request):
    order_id = "CP57"
    sent = new_order_staff_mail(order_id)
    print(sent)
    # print(nueva_orden_mail_client(order_id))

    qs = Order.objects.filter(order_id=order_id)
    context = {"order": qs.first()}

    return render(request, "mails/orders/new_order_staff.html", context)


def guess_checkout_page(request):
    if request.user.is_authenticated:
        return redirect('orders:address')

    if request.method == "POST":
        next_url = request.POST.get('next_url', None)
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            print("next_url ", next_url is None)
            if next_url is None:
                return redirect('/')
            return redirect(next_url)
    else:
        form = AuthenticationForm(request)
        next_url = request.GET.get('next', "/")

    context = {
        "title": "Log In",
        "form": form,
        "next_url": next_url
    }
    return render(request, "orders/guess_checkout.html", context)
