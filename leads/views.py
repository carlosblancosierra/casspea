from django.shortcuts import redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import NewsletterSubscriberForm
from .models import NewsletterSubscriber
from django.template.loader import render_to_string
from django.contrib.staticfiles.storage import staticfiles_storage
from django.utils.html import strip_tags


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterSubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            subscriber = NewsletterSubscriber.objects.filter(email=email).first()
            if not subscriber:
                subscriber = form.save()

            # Send the email with the discount code
            subject = 'CassPea | 15% OFF code'
            html_message = render_to_string('emails/newsletter_subscription.html', {})
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [subscriber.email]
            send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

            messages.success(request, 'Thank you, check your email for the discount code.')
        else:
            messages.error(request, 'Invalid email. Please enter a valid email address.')

    return redirect('/')
