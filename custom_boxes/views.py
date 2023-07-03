from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomBoxLogoForm

from .models import CustomBoxLogo


# Create your views here.
def test_page(request):
    if request.method == 'POST':
        form = CustomBoxLogoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            # return redirect('success')
    else:
        form = CustomBoxLogoForm()

    context = {
        'form': form
    }
    return render(request, 'custom_boxes/test.html', context)


def box_preview_page(request, logo_id=1):
    logo = get_object_or_404(CustomBoxLogo, id=logo_id)

    context = {
        'logo': logo,
    }

    return render(request, 'custom_boxes/preview.html', context)
