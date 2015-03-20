# -*- coding: latin-1 -*-
from django.contrib import admin

from principal.models import *


# Register your models here.
admin.site.register(Administrator)
admin.site.register(Category)
admin.site.register(Venue)
admin.site.register(Feedback)
# admin.site.register(City)
admin.site.register(Trip)
admin.site.register(Traveller)
admin.site.register(Likes)
admin.site.register(Day)
admin.site.register(VenueDay)
admin.site.register(Comment)
admin.site.register(Judges)
admin.site.register(Payment)
admin.site.register(CoinHistory)
admin.site.register(Schedule)
admin.site.register(Assessment)