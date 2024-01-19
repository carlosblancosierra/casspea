from django.shortcuts import render, redirect
from leads.forms import ContactForm
from django.contrib import messages

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import send_mail
from boxes.models import Box, BoxSize
from flavours.models import PreBuildFlavour, Flavour, FlavourChoice

FAQS = [
        {"question": "They are too pretty to eat.",
         "answer": "Not really a question, but we get this a lot. We promise that they taste better than they look. Imagine that 😊"},
        {"question": "What is your shipping policy?",
         "answer": "We offer 24-hour tracked Royal Mail. Because of the delicate nature of our product, we need to guarantee quick delivery. You will be able to track your package the entire way."},
        {"question": "Where should I store them?",
         "answer": "Normally, you can put them in a cool place, such as a cupboard. We do not recommend putting them in the fridge."},
        {"question": "What if it's really hot?",
         "answer": "On the few weeks that we actually get some proper heat, then we do recommend placing them in the fridge. We do, however, advise that they are wrapped in plastic to preserve them as best as possible. If you are conscious about the environment, then we recommend putting them inside a sealed container or a bag."},
        {"question": "Do you ship internationally?",
         "answer": "At the moment, we only ship within the UK."},
        {"question": "Can I choose my own flavours?",
         "answer": "Absolutely, it is one of the coolest things about our business. You can select and see a picture of the chocolate, so you can choose by flavour, or colour, or both. You can also select one of our pre-packed boxes. We offer nut-free, gluten-free, and alcohol-free options."},
        {"question": "How long do they last?",
         "answer": "We advise that they are consumed within 2 weeks of arrival. Most of our chocolates do have a longer shelf life than that. However, we know that the fresher they are, the better they taste."},
        {"question": "Can I order for a future date?",
         "answer": "Yes. Another cool feature that we offer is the ability to select your shipping date. This option is found at checkout."},
        {"question": "What if I need many boxes?",
         "answer": "Our website is programmed to give a generous discount to all orders over 10 boxes."},
        {"question": "What if I need more than that and a bigger discount?",
         "answer": "Please contact us at <a href='mailto:info@casspea.co.uk' class='text-underline my-orange-text'>info@casspea.co.uk</a> "
                   "or send us a WhatsApp message at <a href='tel:07859790386' class='text-underline my-orange-text'>07859 790386.</a>"},
        {"question": "Do you do bespoke orders?",
         "answer": "Absolutely, we can personalize your chocolates. Using our software, you can design your chocolate, and we can develop a flavour if we don't already have it. Please contact us for more information at info@casspea.co.uk or send us a WhatsApp message at 07447 990542."},
        {"question": "How long would a bespoke order take?",
         "answer": "We can make things happen very quickly. If we have the flavour and decoration settled, we can produce them in 3-5 days."},
        {"question": "What is your return policy?",
         "answer": "If you are unsatisfied with your order or there was a problem with delivery, we will do everything possible to make sure that you are left satisfied and wanting to come back again. If you have had a negative experience, please contact us directly at info@casspea.co.uk or send us a WhatsApp message at 07447 990542."},
        {"question": "Where are you located?",
         "answer": "Well, we don't have a physical shop. We do everything online. Our kitchen is based in the south of London."},

    ]

def home_page(request):
    context = {}

    return render(request, "home.html", context)


def valentines_day_page(request):
    context = {}

    valentines_boxes_qs = BoxSize.objects.filter(active=True, valentines_box=True)
    context["valentines_boxes_qs"] = valentines_boxes_qs
    context["faqs"] = FAQS

    flavours_qs = Flavour.objects.active()
    context["flavours_qs"] = flavours_qs

    return render(request, "valentines_day.html", context)


def contact_us_page(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message to the database
            contact_message = form.save()

            # Send the email
            subject = 'New Contact Message'
            html_message = render_to_string(
                'emails/contact_form.html', {'obj': contact_message})
            plain_message = strip_tags(html_message)
            from_email = settings.DEFAULT_FROM_EMAIL
            to_email = [settings.CONTACT_EMAIL, 'carlosblancosierra@gmail.com']
            send_mail(subject, plain_message, from_email,
                      to_email, html_message=html_message)

            messages.success(
                request, 'Your message has been sent successfully!')

            return redirect('/')

    # Handle GET request or invalid form
    else:
        form = ContactForm()

    context = {'form': form}
    return render(request, 'contact_us.html', context)


def about_us_page(request):
    context = {
    }

    return render(request, "about_us.html", context)


def privacy_page(request):
    context = {
    }

    return render(request, "privacy.html", context)


def faqs_page(request):
    context = {'faqs': FAQS}

    return render(request, "faq.html", context)
