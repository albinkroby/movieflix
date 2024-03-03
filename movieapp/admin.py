from django.contrib import admin
from .models import MovieCategory, Movie

# Register your models here.
class MovieCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
admin.site.register(MovieCategory, MovieCategoryAdmin)

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'release_date', 'added_by')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'category__name')
    list_filter = ('category', 'release_date', 'added_by')
admin.site.register(Movie, MovieAdmin)