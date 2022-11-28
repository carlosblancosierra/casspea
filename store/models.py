from django.db import models

# Create your models here.
FLAVOURS = (
    ("Praline Feuilletine", "praline_feuilletine"),
    ("Banana Caramel", "banana_caramel"),
    ("Milk Chocolate", "milk_chocolate"),
)

PRE_BUILDS_FLAVOURS = (
    ("Nut Free", "nut_free"),
    ("Gluten Free", "gluten_free"),
    ("Random", "random"),
    ("Alcohol Free", "alcohol_free"),
)

PRE_BUILT = 'pre_built'
PICK_AND_MIX = 'pick_and_mix'
