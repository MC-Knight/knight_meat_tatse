from django.contrib import admin
from rest_api.models import Dish

admin.site.site_header = "Knight meat eats Administration"

admin.site.register(Dish)
