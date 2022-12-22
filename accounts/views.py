from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib import messages

from carts.models import Cart
from orders.models import Order
from addresses.models import Address

from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm

User = settings.AUTH_USER_MODEL


# Create your views here.
def login_page(request):
    # print(request.user)
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
    return render(request, "accounts/login.html", context)


def register_page_local(request):
    next_url = request.GET.get('next_url', None)
    if request.method == 'POST':
        next_url = request.POST.get('next_url', None)
        user_form = CustomUserCreationForm(request.POST or None)
        if user_form.is_valid():
            user_obj = user_form.save()
            login(request, user_obj)
            # print(user_obj)
            # print('next_url: ', next_url)
            messages.success(request, 'User created')
            if next_url:
                return redirect(next_url)
            return redirect('/')
        else:
            messages.error(request, 'Error')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'accounts/register-local.html', {
        "title": "Register",
        'user_form': user_form,
        "next_url": next_url
    })


@staff_member_required
def user_list_page(request):
    User = get_user_model()
    users = User.objects.all()

    context = {
        "users": users,
    }

    return render(request, "accounts/list.html", context)
