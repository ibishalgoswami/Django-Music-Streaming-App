from django.contrib import admin
from .models import LoginLogoutLog

# Register your models here.
# admin.site.register(UserDetail)


@admin.register(LoginLogoutLog)
class Category(admin.ModelAdmin):
    list_display = [field.name for field in LoginLogoutLog._meta.fields]
    list_display_links = [field.name for field in LoginLogoutLog._meta.fields]