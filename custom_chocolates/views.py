from django.shortcuts import render
from .models import ChocolateDesignLayer, ChocolateDesign, UserChocolateDesign


# Create your views here.
def test_page(request):
    design = ChocolateDesign.objects.filter(id=1).first()
    background_options = design.background_options.all()
    layer1_options = design.layer1_options.all()
    layer2_options = design.layer1_options.all()
    layer3_options = design.layer1_options.all()

    context = {
        "design": design,
        "background_options": background_options,
        "layer1_options": layer1_options,
        "layer2_options": layer2_options,
        "layer3_options": layer3_options,

    }

    return render(request, "custom_chocolates/test2.html", context)
