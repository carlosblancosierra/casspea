from django.template.loader import render_to_string, get_template
from django.core.mail import send_mail, mail_managers
from .models import Order
# from jimmiss.settings.production import EMAIL_STATIC_URL
#
#
# def nueva_orden_mail_staff(order_id):
#     qs = Order.objects.filter(order_id=order_id)
#     if qs.exists():
#         order = qs.first()
#         context = {"order": order, "STATIC_URL": EMAIL_STATIC_URL}
#         try:
#             subject = 'JimMiss - Nueva Orden'
#             message = render_to_string('mails/orders/nueva_staff.txt', context)
#             html_message = render_to_string('mails/orders/nueva_staff.html', context)
#             to_mails = ['jimmiss.sistemas@gmail.com']
#             from_mail = 'no-responda@jimmiss.mx'
#
#             staff_mails_sent = send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=from_mail,
#                 recipient_list=to_mails,
#                 fail_silently=False,
#                 html_message=html_message
#             )
#
#             return staff_mails_sent
#         except:
#             pass
#
#
# def nueva_orden_mail_client(order_id):
#     qs = Order.objects.filter(order_id=order_id)
#     if qs.exists():
#         order = qs.first()
#         context = {"order": order, "STATIC_URL": EMAIL_STATIC_URL}
#         try:
#             subject = 'Tu orden de JimMiss.mx'
#             message = render_to_string('mails/orders/nueva_cliente.txt', context)
#             html_message = render_to_string('mails/orders/nueva_cliente.html', context)
#             to_mails = [order.user.email]
#             from_mail = 'no-responda@jimmiss.mx'
#
#             staff_mails_sent = send_mail(
#                 subject=subject,
#                 message=message,
#                 from_email=from_mail,
#                 recipient_list=to_mails,
#                 fail_silently=False,
#                 html_message=html_message
#             )
#
#             return staff_mails_sent
#         except:
#             pass
#     else:
#         pass
