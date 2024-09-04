from rest_framework import serializers
from .models import Flavour, Allergen

class AllergenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Allergen
        fields = ['name', 'slug']  # Include any other fields you want to expose

class FlavourSerializer(serializers.ModelSerializer):
    allergens = AllergenSerializer(many=True, read_only=True)

    class Meta:
        model = Flavour
        fields = ['name', 'slug', 'description', 'mini_description', 'allergens', 'image', 'valentines_flavour', 'updated', 'timestamp', 'active']
