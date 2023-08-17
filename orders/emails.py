from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, mail_managers
from .models import Order
from django.conf import settings
from ebdjango.settings.production import EMAIL_STATIC_URL


def new_order_staff_mail(request, order_id):
    qs = Order.objects.filter(order_id=order_id)
    domain = request.META['HTTP_HOST']
    if qs.exists():
        order = qs.first()
        context = {
            "order": order,
            "STATIC_URL": EMAIL_STATIC_URL,
            "address": order.shipping_address,
            "entries": order.cart_entries.all(),
            "gift_message": order.gift_message,
            "shipping_cost": order.shipping_cost,
            "domain": domain,
        }

        try:
            subject = 'CassPea.co.uk | New Order'
            message = render_to_string('mails/orders/new_order_staff.txt', context)
            html_message = render_to_string('mails/orders/new_order_staff.html', context)
            to_mails = settings.STAFF_EMAILS
            from_mail = 'CassPea <info@casspea.co.uk>'

            staff_mails_sent = send_mail(
                subject=subject,
                message=message,
                from_email=from_mail,
                recipient_list=to_mails,
                fail_silently=False,
                html_message=html_message
            )

            return staff_mails_sent
        except Exception as e:
            # Log the exception using the logger
            print(f"Error sending email: {e}")
            pass


def new_order_client_mail(order_id):
    qs = Order.objects.filter(order_id=order_id)
    if qs.exists():
        order = qs.first()
        context = {"order": order, "STATIC_URL": EMAIL_STATIC_URL}
        try:
            subject = 'Your CassPea.co.uk order'
            message = render_to_string('mails/orders/new_client.txt', context)
            html_message = render_to_string('mails/orders/new_client.html', context)
            to_mails = [order.user.email]
            from_mail = 'CassPea <info@casspea.co.uk>'

            staff_mails_sent = send_mail(
                subject=subject,
                message=message,
                from_email=from_mail,
                recipient_list=to_mails,
                fail_silently=False,
                html_message=html_message
            )

            return staff_mails_sent
        except:
            pass
    else:
        pass
