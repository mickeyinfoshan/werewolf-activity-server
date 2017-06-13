from django.contrib import admin

# Register your models here.
from .models import Activity, Participation

admin.site.register(Activity)
admin.site.register(Participation)
admin.site.site_title = "狼人杀组局"
admin.site.site_header = "狼人杀组局"