from django.contrib import admin
from .models import Users, Events, Bookings

# Register your models here.

admin.site.register(Users)
admin.site.register(Events)
admin.site.register(Bookings)