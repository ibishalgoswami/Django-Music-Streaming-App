from django.contrib import admin
from .models import Category,Song,Listen_Later

admin.site.site_header = "Music-Mania"

@admin.register(Category)
class Category(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]
    list_display_links = [field.name for field in Category._meta.fields]
    fieldsets = (
      ('Category Info', {
          'fields': ('name',)
      }),
   )


@admin.register(Song)
class Song(admin.ModelAdmin):
    list_display = ["title","added_date","cat"]
    search_fields = ("title","description", )
    list_filter = ("cat","added_date", )
    ordering=("id",)
    list_per_page = 5
    radio_fields = {'cat': admin.HORIZONTAL}
    fieldsets = (
      ('Song Info', {
          'fields': ('title','description')
      }),
      ('File Upload', {
          'fields': ('image', 'song')
      }),
      ('Category', {
          'fields': ('cat',)
      }),
   )


@admin.register(Listen_Later)
class Listen_Later(admin.ModelAdmin):
    list_display = ['user','music_id','added_date']
    ordering=("added_date",)
    
    # This will help you to disbale add functionality
    def has_add_permission(self, request):
        return False

    # This will help you to disable delete functionaliyt
    def has_delete_permission(self, request, obj=None):
        return False

    

