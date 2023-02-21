from django.contrib import admin

# Register your models here.
from advertisements.models import Advertisement, Favourite

admin.site.register(Advertisement)
admin.site.register(Favourite)