from django.shortcuts import render, redirect


def home_page(request):
    context = {
    }

    return render(request, "home.html", context)


def contact_us_page(request):
    context = {
    }

    return render(request, "contact_us.html", context)
